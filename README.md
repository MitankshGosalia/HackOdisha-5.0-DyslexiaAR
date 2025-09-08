# DyslexiaAR - Complete Multi-Service Platform

A comprehensive augmented-reality-powered reading aid for dyslexic users, built with modern web technologies and microservices architecture.

## 🚀 Features

### Frontend (Next.js)
- **30+ Responsive Pages** - Complete website with all routes
- **Authentication System** - NextAuth.js with role-based access (User/Therapist/Admin)
- **Live OCR Demo** - Real-time camera capture with text processing
- **Interactive Dashboards** - Role-specific analytics and controls
- **3D Components** - Three.js text models and visualizations
- **Animated Charts** - Real-time performance metrics
- **Video Backgrounds** - Immersive hero sections
- **Image Galleries** - User stories and case studies
- **Text-to-Speech** - Audio support for detected text
- **Responsive Design** - Tailwind CSS with custom theme

### Backend (FastAPI)
- **OCR Processing** - OpenCV + Tesseract text extraction
- **WebSocket Analytics** - Real-time metrics and notifications
- **TTS Integration** - Text-to-speech endpoint
- **User Management** - Authentication and role management
- **Database Integration** - PostgreSQL with Prisma ORM
- **API Documentation** - Auto-generated OpenAPI docs

### Infrastructure
- **Docker Support** - Full containerization
- **PostgreSQL Database** - Production-ready data persistence
- **WebSocket Support** - Real-time communication
- **CI/CD Ready** - Deployment pipeline for Akash Network

## 📁 Project Structure

```
DyslexiaAR/
├── web/                          # Next.js Frontend
│   ├── pages/                    # 30+ pages and routes
│   │   ├── auth/                 # Authentication pages
│   │   ├── dashboard/            # User dashboards
│   │   ├── admin/                # Admin panel
│   │   ├── blog/                 # Blog posts
│   │   ├── case-studies/         # Case studies
│   │   └── ...                   # 20+ more pages
│   ├── components/               # React components
│   │   ├── ThreeText.tsx         # 3D text component
│   │   └── AnimatedChart.tsx     # Chart component
│   ├── lib/                      # Utilities
│   │   └── prisma.ts             # Database client
│   ├── prisma/                   # Database schema
│   │   └── schema.prisma         # Prisma schema
│   └── public/images/            # Static assets
├── services/
│   └── api/                      # FastAPI Backend
│       ├── main.py               # Main API server
│       ├── requirements.txt      # Python dependencies
│       └── Dockerfile            # Container config
├── infra/                        # Infrastructure
│   └── docker-compose.yml        # Multi-service setup
├── frontend/                     # Legacy static site
└── backend/                      # Legacy FastAPI + SQLite
```

## 🛠️ Prerequisites

- **Node.js 18+** - For Next.js frontend
- **Python 3.11+** - For FastAPI backend
- **PostgreSQL 15+** - For database
- **Docker** (optional) - For containerized deployment
- **Tesseract OCR** - For text recognition

### Install Tesseract OCR

**Windows:**
```bash
# Download from: https://github.com/UB-Mannheim/tesseract/wiki
# Or use chocolatey:
choco install tesseract
```

**macOS:**
```bash
brew install tesseract
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt-get install tesseract-ocr
```

## 🚀 Quick Start

### Option 1: Docker Compose (Recommended)

```bash
# Clone and start all services
git clone <repository-url>
cd DyslexiaAR
docker compose -f infra/docker-compose.yml up -d --build

# Access the application:
# Web: http://localhost:3000
# API: http://localhost:8080
# Database: localhost:5432
```

### Option 2: Manual Setup

#### 1. Database Setup
```bash
# Install PostgreSQL and create database
createdb dyslexiaar
# Or using psql:
psql -c "CREATE DATABASE dyslexiaar;"
```

#### 2. Frontend Setup
```bash
cd web

# Install dependencies
npm install

# Set up environment variables
cp .env.example .env.local
# Edit .env.local with your database URL

# Set up database
npx prisma migrate dev

# Start development server
npm run dev
```

#### 3. Backend Setup
```bash
cd services/api

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Start API server
uvicorn main:app --host 0.0.0.0 --port 8080 --reload
```

## 🔧 Environment Variables

### Frontend (.env.local)
```env
NEXT_PUBLIC_API_URL=http://localhost:8080
NEXTAUTH_URL=http://localhost:3000
NEXTAUTH_SECRET=your-secret-key-change-in-production
DATABASE_URL=postgresql://username:password@localhost:5432/dyslexiaar
```

### Backend
```env
# Optional: Set Tesseract path if not in PATH
TESSERACT_CMD=/usr/bin/tesseract

# Optional: Google Cloud TTS credentials
GOOGLE_APPLICATION_CREDENTIALS=path/to/service-account.json
```

## 📱 Usage

### 1. Access the Application
- Open http://localhost:3000
- Create an account or sign in
- Choose your role: User, Therapist, or Admin

### 2. Try the Demo
- Navigate to the Demo page
- Allow camera access
- Click "Start Analysis" to begin OCR processing
- Adjust typography settings in the sidebar
- Enable TTS for audio feedback

### 3. Explore Dashboards
- **User Dashboard**: View your analysis history and progress
- **Therapist Dashboard**: Monitor patient progress and sessions
- **Admin Dashboard**: System metrics and user management

## 🔌 API Endpoints

### Core Endpoints
- `GET /health` - Health check
- `POST /process-video` - OCR text processing
- `POST /tts` - Text-to-speech generation
- `GET /stats` - System statistics
- `POST /feedback` - User feedback submission

### WebSocket
- `ws://localhost:8080/ws/analytics` - Real-time analytics

### Authentication
- `POST /api/auth/signup` - User registration
- `POST /api/auth/signin` - User login
- `GET /api/auth/session` - Session info

## 🎨 Customization

### Adding New Pages
```bash
# Create new page
touch web/pages/new-page.tsx

# Add to navigation
# Edit web/pages/index.tsx or create layout component
```

### Styling
- Edit `web/tailwind.config.js` for theme customization
- Modify `web/styles/globals.css` for global styles
- Use Tailwind classes for component styling

### Database Schema
```bash
# Modify schema
nano web/prisma/schema.prisma

# Apply changes
npx prisma migrate dev

# Generate client
npx prisma generate
```

## 🚀 Deployment

### Docker Deployment
```bash
# Build and deploy
docker compose -f infra/docker-compose.yml up -d --build

# Scale services
docker compose -f infra/docker-compose.yml up -d --scale api=3
```

### Vercel (Frontend)
```bash
# Install Vercel CLI
npm i -g vercel

# Deploy
cd web
vercel --prod
```

### Railway/Render (Backend)
```bash
# Connect your repository
# Set environment variables
# Deploy automatically on push
```

### Akash Network
```bash
# Deploy to Akash Network
# See infra/akash/ for deployment manifests
```

## 🧪 Testing

### Frontend Tests
```bash
cd web
npm test
npm run test:e2e
```

### Backend Tests
```bash
cd services/api
pytest
```

### Integration Tests
```bash
# Test full stack
npm run test:integration
```

## 📊 Monitoring

### WebSocket Analytics
- Real-time connection tracking
- Analysis completion notifications
- System health monitoring

### Database Monitoring
```bash
# Prisma Studio
npx prisma studio

# Database queries
npx prisma db seed
```

## 🔒 Security

### Authentication
- NextAuth.js with secure sessions
- Role-based access control
- CSRF protection

### API Security
- CORS configuration
- Input validation
- Rate limiting (recommended for production)

### Database Security
- Connection encryption
- User permissions
- Backup strategies

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📄 License

MIT License - see LICENSE file for details

## 🆘 Support

- **Documentation**: Check this README and inline comments
- **Issues**: Create GitHub issues for bugs
- **Discussions**: Use GitHub Discussions for questions
- **Email**: support@dyslexiaar.com

## 🎯 Roadmap

- [ ] Google Cloud TTS integration
- [ ] Orkes Conductor orchestration
- [ ] Mobile app (React Native)
- [ ] Advanced analytics dashboard
- [ ] Multi-language support
- [ ] Offline mode
- [ ] Voice commands
- [ ] AR glasses integration

---

**Built with ❤️ for the dyslexic community**