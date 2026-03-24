import express, { Express, Request, Response, NextFunction } from 'express';
import cors from 'cors';
import helmet from 'helmet';
import morgan from 'morgan';
import dotenv from 'dotenv';
import path from 'path';

import quizRoutes from './routes/quiz.js';
import analyticsRoutes from './routes/analytics.js';
import authRoutes from './routes/auth.js';

dotenv.config();

const app: Express = express();
const PORT = process.env.PORT || 3001;

// Middleware
app.use(helmet());
app.use(cors({
  origin: process.env.CORS_ORIGINS?.split(',') || ['http://localhost:3000'],
  credentials: true,
}));
app.use(morgan('dev'));
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

// Health check
app.get('/health', (_req: Request, res: Response) => {
  res.json({ 
    status: 'healthy', 
    version: '1.0.0',
    service: 'EduEquity Express API'
  });
});

// API Routes
app.use('/api/v1/quizzes', quizRoutes);
app.use('/api/v1/analytics', analyticsRoutes);
app.use('/api/v1/auth', authRoutes);

// Serve static frontend (simple Tailwind-based prototype)
const publicDir = path.join(__dirname, '..', 'public');
app.use(express.static(publicDir));

// Frontend routes (friendly URLs)
app.get('/', (_req: Request, res: Response) => {
  res.sendFile(path.join(publicDir, 'index.html'));
});

app.get('/login', (_req: Request, res: Response) => {
  res.sendFile(path.join(publicDir, 'login.html'));
});

app.get('/register', (_req: Request, res: Response) => {
  res.sendFile(path.join(publicDir, 'register.html'));
});

app.get('/dashboard', (_req: Request, res: Response) => {
  res.sendFile(path.join(publicDir, 'dashboard-principal.html'));
});

app.get('/dashboard/principal', (_req: Request, res: Response) => {
  res.sendFile(path.join(publicDir, 'dashboard-principal.html'));
});

app.get('/dashboard/teacher', (_req: Request, res: Response) => {
  res.sendFile(path.join(publicDir, 'dashboard-teacher.html'));
});

app.get('/dashboard/student', (_req: Request, res: Response) => {
  res.sendFile(path.join(publicDir, 'dashboard-student.html'));
});

// Root endpoint
// Root API info (mounted under /api or accessed at /api/info)
app.get('/api/info', (_req: Request, res: Response) => {
  res.json({
    message: 'EduEquity OS Express API',
    version: '1.0.0',
    docs: '/api/v1',
    endpoints: {
      quizzes: '/api/v1/quizzes',
      analytics: '/api/v1/analytics'
    }
  });
});

// 404 handler
app.use((_req: Request, res: Response) => {
  res.status(404).json({ error: 'Not Found' });
});

// Error handler
app.use((err: Error, _req: Request, res: Response, _next: NextFunction) => {
  console.error('Error:', err.message);
  res.status(500).json({ error: 'Internal Server Error', message: err.message });
});

// Start server
app.listen(PORT, () => {
  console.log(`🚀 EduEquity Express API running on port ${PORT}`);
  console.log(`📋 Health check: http://localhost:${PORT}/health`);
});

export default app;

