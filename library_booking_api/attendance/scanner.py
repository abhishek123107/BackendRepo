"""QR Code Scanner Utilities for Attendance System"""

import cv2
import numpy as np
from pyzbar import pyzbar
from PIL import Image
import io
import base64
import json
import time
from django.utils import timezone
from django.core.exceptions import ValidationError
from .models import AttendanceSession, AttendanceRecord
from accounts.models import User


class QRCodeScanner:
    """QR Code Scanner for Attendance System"""
    
    def __init__(self):
        self.scanner_active = False
        
    def scan_qr_from_image(self, image_data):
        """
        Scan QR code from image data (base64 or file)
        Returns: dict with qr_data, confidence, and error
        """
        try:
            # Convert base64 to image if needed
            if isinstance(image_data, str) and image_data.startswith('data:image'):
                # Remove data URL prefix
                image_data = image_data.split(',')[1]
                image_bytes = base64.b64decode(image_data)
                image = Image.open(io.BytesIO(image_bytes))
            else:
                # Assume it's a file path or PIL Image
                image = image_data if isinstance(image_data, Image.Image) else Image.open(image_data)
            
            # Convert to OpenCV format
            opencv_image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
            
            # Scan for QR codes
            qr_codes = pyzbar.decode(opencv_image)
            
            if qr_codes:
                qr_code = qr_codes[0]  # Take first QR code found
                return {
                    'success': True,
                    'qr_data': qr_code.data.decode('utf-8'),
                    'confidence': self._calculate_confidence(qr_code),
                    'position': {
                        'x': qr_code.rect.left,
                        'y': qr_code.rect.top,
                        'width': qr_code.rect.width,
                        'height': qr_code.rect.height
                    },
                    'quality': qr_code.quality
                }
            else:
                return {
                    'success': False,
                    'error': 'No QR code found in image',
                    'confidence': 0.0
                }
                
        except Exception as e:
            return {
                'success': False,
                'error': f'Scanning error: {str(e)}',
                'confidence': 0.0
            }
    
    def scan_qr_from_camera(self, camera_index=0, timeout=30):
        """
        Scan QR code from camera feed
        Returns: dict with qr_data, confidence, and error
        """
        cap = cv2.VideoCapture(camera_index)
        if not cap.isOpened():
            return {
                'success': False,
                'error': 'Cannot access camera',
                'confidence': 0.0
            }
        
        self.scanner_active = True
        start_time = time.time()
        
        try:
            while self.scanner_active and (time.time() - start_time) < timeout:
                ret, frame = cap.read()
                if not ret:
                    continue
                
                # Scan for QR codes in frame
                qr_codes = pyzbar.decode(frame)
                
                if qr_codes:
                    qr_code = qr_codes[0]
                    cap.release()
                    return {
                        'success': True,
                        'qr_data': qr_code.data.decode('utf-8'),
                        'confidence': self._calculate_confidence(qr_code),
                        'position': {
                            'x': qr_code.rect.left,
                            'y': qr_code.rect.top,
                            'width': qr_code.rect.width,
                            'height': qr_code.rect.height
                        },
                        'quality': qr_code.quality,
                        'timestamp': timezone.now().isoformat()
                    }
                
                # Display frame with QR detection (optional)
                cv2.imshow('QR Scanner', frame)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
            
            cap.release()
            cv2.destroyAllWindows()
            
            return {
                'success': False,
                'error': 'No QR code detected within timeout period',
                'confidence': 0.0
            }
            
        except Exception as e:
            cap.release()
            cv2.destroyAllWindows()
            return {
                'success': False,
                'error': f'Camera scanning error: {str(e)}',
                'confidence': 0.0
            }
    
    def stop_scanning(self):
        """Stop active camera scanning"""
        self.scanner_active = False
    
    def _calculate_confidence(self, qr_code):
        """Calculate confidence score for QR code detection"""
        # Base confidence from quality
        confidence = qr_code.quality / 100.0 if qr_code.quality else 0.5
        
        # Adjust based on QR code size (larger = more reliable)
        area = qr_code.rect.width * qr_code.rect.height
        if area > 10000:  # Large QR code
            confidence += 0.2
        elif area > 5000:  # Medium QR code
            confidence += 0.1
        
        # Adjust based on data length (longer = more complex)
        data_length = len(qr_code.data)
        if data_length > 20:
            confidence += 0.1
        
        return min(confidence, 1.0)
    
    def process_attendance_scan(self, qr_data, user, scan_location=None, device_info=None):
        """
        Process QR code scan for attendance
        Returns: dict with success, attendance_record, and message
        """
        try:
            # Parse QR data format: "attendance:TOKEN"
            if not qr_data.startswith('attendance:'):
                return {
                    'success': False,
                    'error': 'Invalid QR code format for attendance',
                    'attendance_record': None
                }
            
            token = qr_data.split(':')[1]
            
            # Find session by QR token
            try:
                session = AttendanceSession.objects.get(qr_code_token=token)
            except AttendanceSession.DoesNotExist:
                return {
                    'success': False,
                    'error': 'Invalid attendance session',
                    'attendance_record': None
                }
            
            # Check if user already has attendance record for this session
            attendance_record, created = AttendanceRecord.objects.get_or_create(
                user=user,
                session=session,
                defaults={
                    'status': 'absent',
                    'verification_method': 'scanner'
                }
            )
            
            if not created:
                return {
                    'success': False,
                    'error': 'Attendance already recorded for this session',
                    'attendance_record': attendance_record
                }
            
            # Process the QR scan
            success = attendance_record.scan_qr_code(
                qr_token=token,
                scan_location=scan_location,
                device_info=device_info
            )
            
            if success:
                return {
                    'success': True,
                    'message': 'Attendance marked successfully',
                    'attendance_record': attendance_record,
                    'session': session.title,
                    'check_in_time': attendance_record.check_in_time,
                    'status': attendance_record.status
                }
            else:
                return {
                    'success': False,
                    'error': 'Failed to process attendance',
                    'attendance_record': None
                }
                
        except Exception as e:
            return {
                'success': False,
                'error': f'Processing error: {str(e)}',
                'attendance_record': None
            }


# Global scanner instance
qr_scanner = QRCodeScanner()
