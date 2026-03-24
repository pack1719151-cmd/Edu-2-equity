import { Router, Request, Response } from 'express';
import { v4 as uuidv4 } from 'uuid';

const router = Router();

// In-memory user store (prototype only)
type User = { id: string; name: string; email: string; password: string; role?: string };
const users = new Map<string, User>();

router.post('/register', (req: Request, res: Response) => {
  const { name, email, password, role } = req.body || {};
  if (!email || !password || !name) {
    return res.status(400).json({ success: false, message: 'Missing required fields' });
  }
  if (Array.from(users.values()).some(u => u.email === email)) {
    return res.status(409).json({ success: false, message: 'Email already registered' });
  }
  const id = uuidv4();
  const user: User = { id, name, email, password, role: role || 'student' };
  users.set(id, user);
  return res.json({ success: true, user: { id: user.id, name: user.name, email: user.email, role: user.role } });
});

router.post('/login', (req: Request, res: Response) => {
  const { email, password } = req.body || {};
  if (!email || !password) {
    return res.status(400).json({ success: false, message: 'Missing email or password' });
  }
  const found = Array.from(users.values()).find(u => u.email === email && u.password === password);
  if (!found) {
    return res.status(401).json({ success: false, message: 'Invalid credentials' });
  }
  // Prototype: return user info (no real session/JWT)
  return res.json({ success: true, user: { id: found.id, name: found.name, email: found.email, role: found.role } });
});

export default router;
