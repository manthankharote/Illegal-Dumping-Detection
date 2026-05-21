const express = require('express');
const router = express.Router();
const User = require('../models/User');
const { authenticate, authorize } = require('../middleware/auth');
const auditLog = require('../middleware/audit');
const { sendSuccess, sendError, asyncHandler, paginate, paginateMeta } = require('../utils/helpers');

// GET /api/users - List all users (superadmin)
router.get('/', authenticate, authorize('superadmin'), asyncHandler(async (req, res) => {
  const { page = 1, limit = 20, role, ward } = req.query;
  const { skip } = paginate({}, page, limit);
  const filter = {};
  if (role) filter.role = role;
  if (ward) filter.ward = ward;

  const total = await User.countDocuments(filter);
  const users = await User.find(filter)
    .sort({ createdAt: -1 })
    .skip(skip)
    .limit(parseInt(limit));

  sendSuccess(res, 200, users, 'Users fetched', paginateMeta(total, page, limit));
}));

// PUT /api/users/:id/role - Change user role (superadmin)
router.put('/:id/role', authenticate, authorize('superadmin'), auditLog('CHANGE_ROLE', 'User'),
  asyncHandler(async (req, res) => {
    const { role } = req.body;
    if (!['citizen', 'worker', 'admin', 'superadmin'].includes(role)) {
      return sendError(res, 400, 'Invalid role');
    }
    const user = await User.findByIdAndUpdate(req.params.id, { role }, { new: true });
    if (!user) return sendError(res, 404, 'User not found');
    sendSuccess(res, 200, user, 'Role updated');
  })
);

// PUT /api/users/:id/deactivate - Deactivate user (superadmin)
router.put('/:id/deactivate', authenticate, authorize('superadmin'), auditLog('DEACTIVATE_USER', 'User'),
  asyncHandler(async (req, res) => {
    const user = await User.findByIdAndUpdate(req.params.id, { isActive: false }, { new: true });
    if (!user) return sendError(res, 404, 'User not found');
    sendSuccess(res, 200, user, 'User deactivated');
  })
);

// GET /api/users/workers - Get all workers (admin)
router.get('/workers', authenticate, authorize('admin', 'superadmin'), asyncHandler(async (req, res) => {
  const { ward } = req.query;
  const filter = { role: 'worker', isActive: true };
  if (ward) filter.ward = ward;
  const workers = await User.find(filter).sort({ name: 1 });
  sendSuccess(res, 200, workers, 'Workers fetched');
}));

// GET /api/users/ward-staff - Get all workers + admins in logged-in admin's ward
router.get('/ward-staff', authenticate, authorize('admin', 'superadmin'), asyncHandler(async (req, res) => {
  const ward = req.user.ward;
  if (!ward) return sendError(res, 400, 'No ward assigned to your account');

  const staff = await User.find({ 
    ward, 
    role: { $in: ['worker', 'admin'] }, 
    isActive: true 
  }).select('name email phone role ward').sort({ role: 1, name: 1 });

  sendSuccess(res, 200, staff, 'Ward staff fetched');
}));

// PUT /api/users/:id/phone - Admin updates a ward member's phone number
router.put('/:id/phone', authenticate, authorize('admin', 'superadmin'), asyncHandler(async (req, res) => {
  const { phone } = req.body;
  if (!phone) return sendError(res, 400, 'Phone number is required');

  // Ensure admin can only update users in their own ward
  const targetUser = await User.findById(req.params.id);
  if (!targetUser) return sendError(res, 404, 'User not found');
  
  if (req.user.role === 'admin' && targetUser.ward !== req.user.ward) {
    return sendError(res, 403, 'You can only update staff in your own ward');
  }

  // Normalize phone: prefix 91 if needed
  let normalizedPhone = phone.replace(/\D/g, '');
  if (normalizedPhone.length === 10) normalizedPhone = '91' + normalizedPhone;

  const updated = await User.findByIdAndUpdate(
    req.params.id,
    { phone: normalizedPhone },
    { new: true }
  ).select('name email phone role ward');

  sendSuccess(res, 200, updated, 'Phone number updated');
}));

module.exports = router;
