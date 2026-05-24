const express = require('express');
const router = express.Router();
const axios = require('axios');
const { authenticate, authorize } = require('../middleware/auth');

/**
 * @route   GET /api/cctv/stream
 * @desc    Proxies the live YOLO-processed MJPEG stream from local Python engine
 * @access  Private (Admins & Superadmins only)
 */
router.get('/stream', authenticate, authorize('admin', 'superadmin'), async (req, res) => {
  // Internal URL pointing to the local Python FastAPI stream server
  const pythonStreamUrl = process.env.PYTHON_STREAM_URL || 'http://127.0.0.1:7861/stream';

  try {
    const response = await axios({
      method: 'get',
      url: pythonStreamUrl,
      responseType: 'stream',
      timeout: 15000 // 15 seconds connection timeout
    });

    // Forward the content type header (multipart/x-mixed-replace; boundary=frame)
    const contentType = response.headers['content-type'] || 'multipart/x-mixed-replace; boundary=frame';
    res.setHeader('Content-Type', contentType);

    // Pipe the python MJPEG stream directly to the response client
    response.data.pipe(res);

    // If client closes connection (e.g. leaves page), terminate the upstream stream request
    req.on('close', () => {
      if (response.data && typeof response.data.destroy === 'function') {
        response.data.destroy();
      }
    });

  } catch (error) {
    console.error('❌ CCTV Stream proxy error:', error.message);
    res.status(502).json({ 
      success: false, 
      message: 'Failed to connect to internal CCTV streaming engine. Make sure the YOLO script is running.' 
    });
  }
});

module.exports = router;
