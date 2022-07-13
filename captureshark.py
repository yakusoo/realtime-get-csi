import pyshark

cap = pyshark.RemoteCapture("10.10.201.44", 'mon0')
cap.sniff(timeout=50)
cap