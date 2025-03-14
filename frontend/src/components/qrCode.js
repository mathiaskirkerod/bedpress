import React from 'react';
import { useLocation } from 'react-router-dom';
import QRCode from "react-qr-code";


const QRCodeComponent = () => {
  const location = useLocation();
  const currentUrl = `${window.location.origin}${location.pathname}`;

  return (
    <div className="flex justify-end mb-4">
      <div className="bg-white p-2 rounded shadow-md">
        <div className="text-sm text-gray-500 mb-1">Scan to submit:</div>
        <div className="w-24 h-24 bg-gray-200 flex items-center justify-center border border-gray-300">
          <QRCode value={currentUrl} />
        </div>
      </div>
    </div>
  );
};

export default QRCodeComponent;