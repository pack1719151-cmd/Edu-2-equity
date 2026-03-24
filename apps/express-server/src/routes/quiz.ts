import { Router, Request, Response } from 'express';
import { v4 as uuidv4 } from 'uuid';
import { z } from 'zod';

const router = Router();

// In-memory storage for demo (replace with database in production)
interface Question {
  id: string;
  text: string;
  type: 'multiple_choice' | 'true_false' | 'short_answer';
  options?: string[];
  correctAnswer: string;
  points: number;
}

interface Quiz {
  id: string;
  title: string;
  description: string;
  classId: string;
  teacherId: string;
  questions: Question[];
  timeLimit: number; // in minutes
  createdAt: string;
  status: 'draft' | 'published' | 'closed';
}

// Mock data
const quizzes: Quiz[] = [
  {
    id: '1',
    title: 'Mathematics Fundamentals',
    description: 'Basic algebra and geometry questions',
    classId: 'class-1',
    teacherId: 'teacher-1',
    questions: [
      {
        id: 'q1',
        text: 'What is 2 + 2?',
        type: 'multiple_choice',
        options: ['3', '4', '5', '6'],
        correctAnswer: '4',
        points: 10
      },
      {
        id: 'q2',
        text: 'A triangle has 3 sides.',
        type: 'true_false',
        correctAnswer: 'true',
        points: 5
      }
    ],
    timeLimit: 30,
    createdAt: new Date().toISOString(),
    status: 'published'
  }
];

// Validation schemas
const createQuizSchema = z.object({
  title: z.string().min(1).max(200),
  description: z.string().max(1000).optional(),
  classId: z.string().min(1),
  teacherId: z.string().min(1),
  questions: z.array(z.object({
    text: z.string().min(1),
    type: z.enum(['multiple_choice', 'true_false', 'short_answer']),
    options: z.array(z.string()).optional(),
    correctAnswer: z.string().min(1),
    points: z.number().int().positive()
  })).min(1),
  timeLimit: z.number().int().positive().max(180).default(30)
});

// Get all quizzes
router.get('/', (_req: Request, res: Response) => {
  res.json({
    success: true,
    data: quizzes,
    total: quizzes.length
  });
});

// Get quiz by ID
router.get('/:id', (req: Request, res: Response) => {
  const quiz = quizzes.find(q => q.id === req.params.id);
  
  if (!quiz) {
    return res.status(404).json({
      success: false,
      error: 'Quiz not found'
    });
  }
  
  res.json({
    success: true,
    data: quiz
  });
});

// Get quizzes by class
router.get('/class/:classId', (req: Request, res: Response) => {
  const classQuizzes = quizzes.filter(q => q.classId === req.params.classId);
  
  res.json({
    success: true,
    data: classQuizzes,
    total: classQuizzes.length
  });
});

// Create new quiz
router.post('/', (req: Request, res: Response) => {
  try {
    const validatedData = createQuizSchema.parse(req.body);
    
    const newQuiz: Quiz = {
      id: uuidv4(),
      ...validatedData,
      createdAt: new Date().toISOString(),
      status: 'draft'
    };
    
    quizzes.push(newQuiz);
    
    res.status(201).json({
      success: true,
      data: newQuiz,
      message: 'Quiz created successfully'
    });
  } catch (error) {
    if (error instanceof z.ZodError) {
      return res.status(400).json({
        success: false,
        error: 'Validation failed',
        details: error.errors
      });
    }
    
    res.status(500).json({
      success: false,
      error: 'Failed to create quiz'
    });
  }
});

// Update quiz
router.put('/:id', (req: Request, res: Response) => {
  const index = quizzes.findIndex(q => q.id === req.params.id);
  
  if (index === -1) {
    return res.status(404).json({
      success: false,
      error: 'Quiz not found'
    });
  }
  
  try {
    const validatedData = createQuizSchema.partial().parse(req.body);
    
    quizzes[index] = {
      ...quizzes[index],
      ...validatedData
    };
    
    res.json({
      success: true,
      data: quizzes[index],
      message: 'Quiz updated successfully'
    });
  } catch (error) {
    if (error instanceof z.ZodError) {
      return res.status(400).json({
        success: false,
        error: 'Validation failed',
        details: error.errors
      });
    }
    
    res.status(500).json({
      success: false,
      error: 'Failed to update quiz'
    });
  }
});

// Publish quiz
router.patch('/:id/publish', (req: Request, res: Response) => {
  const quiz = quizzes.find(q => q.id === req.params.id);
  
  if (!quiz) {
    return res.status(404).json({
      success: false,
      error: 'Quiz not found'
    });
  }
  
  if (quiz.status === 'published') {
    return res.status(400).json({
      success: false,
      error: 'Quiz is already published'
    });
  }
  
  quiz.status = 'published';
  
  res.json({
    success: true,
    data: quiz,
    message: 'Quiz published successfully'
  });
});

// Delete quiz
router.delete('/:id', (req: Request, res: Response) => {
  const index = quizzes.findIndex(q => q.id === req.params.id);
  
  if (index === -1) {
    return res.status(404).json({
      success: false,
      error: 'Quiz not found'
    });
  }
  
  quizzes.splice(index, 1);
  
  res.json({
    success: true,
    message: 'Quiz deleted successfully'
  });
});

export default router;

