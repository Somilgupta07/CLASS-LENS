<div align="center">

<img src="https://i.ibb.co/YTYGn5qV/logo.png" height="90" alt="ClassLens Logo" />

# ClassLens

### AI-Powered Attendance System

**Take attendance in 3 seconds — not 3 minutes.**
Face recognition + voice biometrics, built on Streamlit.

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat-square&logo=python&logoColor=white)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.x-FF4B4B?style=flat-square&logo=streamlit&logoColor=white)](https://streamlit.io)
[![Supabase](https://img.shields.io/badge/Supabase-PostgreSQL-3ECF8E?style=flat-square&logo=supabase&logoColor=white)](https://supabase.com)
[![License](https://img.shields.io/badge/License-MIT-00C896?style=flat-square)](LICENSE)

[Live Demo](#) · [Report Bug](../../issues) · [Request Feature](../../issues)

</div>

---

## What is ClassLens?

ClassLens is a classroom attendance system that replaces manual roll calls with AI. Teachers snap a photo of the class or run a voice roll-call — ClassLens identifies every student automatically using face recognition and voice biometrics, logs the results, and gives teachers exportable records instantly.

No app installs for students. No hardware required. Just a camera and a browser.

---

## Features

**For Teachers**
- 📸 **FaceID Attendance** — upload one or more class photos; AI identifies all enrolled students
- 🎙️ **Voice ID Attendance** — students say "Present"; AI matches voice signatures in real-time
- 📚 **Subject Management** — create subjects, auto-generate QR codes and shareable join links
- 📊 **Attendance Records** — full history with timestamps, confidence scores, and CSV export
- 🔐 **Secure Auth** — username/password login with encrypted credentials

**For Students**
- 👤 **FaceID Login** — log in by looking at the camera, no password needed
- 🔗 **QR Enrollment** — join a course by scanning a QR code or clicking a link
- 📈 **Personal Dashboard** — track attendance percentage across all enrolled subjects
- 🎤 **Voice Registration** — enroll voice once, recognized forever

---

## Tech Stack

| Layer | Technology |
|---|---|
| Frontend | Streamlit |
| Landing Page | Flask + HTML/CSS |
| Face Recognition | `face_recognition`, `dlib` |
| Voice Biometrics | `resemblyzer`, `librosa` |
| Database | Supabase (PostgreSQL) |
| Auth & Storage | Supabase Auth + Storage |
| Deployment | Streamlit Community Cloud |

---

## Project Structure

```
classlens/
├── app.py                          # Entry point
├── requirements.txt
├── .streamlit/
│   └── config.toml                 # Theme config
│
├── src/
│   ├── screens/
│   │   ├── home_screen.py          # Landing / role selection
│   │   ├── teacher_screen.py       # Teacher dashboard + flows
│   │   └── student_screen.py       # Student dashboard + FaceID login
│   │
│   ├── components/
│   │   ├── header.py
│   │   ├── footer.py
│   │   ├── subject_card.py
│   │   ├── dialog_create_subject.py
│   │   ├── dialog_share_subject.py
│   │   ├── dialog_add_photo.py
│   │   ├── dialog_attendance_results.py
│   │   ├── dialog_voice_attendance.py
│   │   ├── dialog_enroll.py
│   │   └── dialog_auto_enroll.py
│   │
│   ├── pipelines/
│   │   ├── face_pipelines.py       # Face detection, embedding, classifier
│   │   └── voice_pipelines.py      # Voice embedding via resemblyzer
│   │
│   ├── database/
│   │   ├── config.py               # Supabase client init
│   │   └── db.py                   # All DB queries
│   │
│   └── ui/
│       └── base_layout.py          # Global CSS / theme
│
└── landing/                        # Flask landing page (optional)
    ├── app.py
    ├── templates/index.html
    └── static/
```

---

## Getting Started

### Prerequisites

- Python 3.10 or higher
- A [Supabase](https://supabase.com) project (free tier works)
- `cmake` installed (required by `dlib`)

```bash
# macOS
brew install cmake

# Ubuntu / Debian
sudo apt-get install cmake build-essential
```

### Installation

**1. Clone the repo**
```bash
git clone https://github.com/your-username/classlens.git
cd classlens
```

**2. Create a virtual environment**
```bash
python -m venv venv
source venv/bin/activate        # macOS / Linux
venv\Scripts\activate           # Windows
```

**3. Install dependencies**
```bash
pip install -r requirements.txt
```

**4. Set up environment variables**

Create a `.env` file in the project root:
```env
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your-anon-key
```

Or add them directly to `.streamlit/secrets.toml`:
```toml
SUPABASE_URL = "https://your-project.supabase.co"
SUPABASE_KEY = "your-anon-key"
```

**5. Run the app**
```bash
streamlit run app.py
```

Open [http://localhost:8501](http://localhost:8501)

---

## Database Setup

Run the following SQL in your Supabase SQL editor to create the required tables:

```sql
-- Teachers
create table teachers (
  teacher_id uuid primary key default gen_random_uuid(),
  username text unique not null,
  password text not null,
  name text not null,
  created_at timestamptz default now()
);

-- Students
create table students (
  student_id serial primary key,
  name text not null,
  face_embedding jsonb,
  voice_embedding jsonb,
  created_at timestamptz default now()
);

-- Subjects
create table subjects (
  subject_id uuid primary key default gen_random_uuid(),
  teacher_id uuid references teachers(teacher_id),
  name text not null,
  subject_code text unique not null,
  section text,
  total_students int default 0,
  total_classes int default 0,
  created_at timestamptz default now()
);

-- Subject–Student enrollment
create table subject_students (
  id serial primary key,
  subject_id uuid references subjects(subject_id),
  student_id int references students(student_id),
  enrolled_at timestamptz default now()
);

-- Attendance logs
create table attendance (
  id serial primary key,
  student_id int references students(student_id),
  subject_id uuid references subjects(subject_id),
  timestamp timestamptz,
  is_present boolean default false
);
```

---

## How It Works

### Face Attendance Flow
```
Teacher uploads class photo(s)
        ↓
face_recognition detects all faces
        ↓
Each face → 128-dim embedding
        ↓
Nearest-neighbor match against enrolled students
        ↓
Present / Absent logged to Supabase
```

### Voice Attendance Flow
```
Teacher starts voice roll-call
        ↓
Students say "Present" one by one
        ↓
resemblyzer extracts d-vector embedding
        ↓
Cosine similarity against stored voice embeddings
        ↓
Match → marked Present
```

### Student QR Enrollment
```
Teacher creates subject → unique join code generated
        ↓
Teacher shares QR / link (?join-code=XXXX)
        ↓
Student opens link → auto-routed to student login
        ↓
After FaceID login → auto-enrolled to subject
```

---

## Keyboard Shortcuts

| Shortcut | Action |
|---|---|
| `Ctrl + Enter` | Login / Submit |
| `Ctrl + Backspace` | Go back to Home / Logout |

---

## Deployment

### Streamlit Community Cloud (recommended, free)

1. Push your repo to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your repo, set `app.py` as the entry point
4. Add your Supabase secrets under **Settings → Secrets**

```toml
SUPABASE_URL = "https://your-project.supabase.co"
SUPABASE_KEY = "your-anon-key"
```

---

## Environment Variables

| Variable | Description | Required |
|---|---|---|
| `SUPABASE_URL` | Your Supabase project URL | ✅ |
| `SUPABASE_KEY` | Supabase anon/public key | ✅ |

---

## Contributing

Contributions are welcome.

1. Fork the repository
2. Create a feature branch — `git checkout -b feature/your-feature`
3. Commit your changes — `git commit -m 'Add your feature'`
4. Push to the branch — `git push origin feature/your-feature`
5. Open a Pull Request

Please keep PRs focused — one feature or fix per PR.

---

## Known Limitations

- Face recognition accuracy drops with poor lighting or low-resolution images
- Voice ID works best in quiet environments
- `dlib` installation can be tricky on Windows — use WSL2 if you hit issues
- Free Supabase tier has a 500MB database limit

---

## License

Distributed under the MIT License. See `LICENSE` for details.

---

<div align="center">

Built with ❤️ for educators everywhere

<img src="https://i.ibb.co/0p9yD7dQ/Gemini-Generated-Image-tsm2a7tsm2a7tsm2-1.png" height="40" alt="Made by AI Todders" />

</div>
