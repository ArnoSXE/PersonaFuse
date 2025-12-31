# PersonaFuse

**PersonaFuse** is a Level-2 OSINT (Open-Source Intelligence) username correlation tool designed to assess whether two online identities are likely operated by the same individual.  
It combines **username similarity**, **platform presence overlap**, **stylometric text analysis**, and **optional facial image matching** to produce a confidence-based assessment.

This project is intended for **ethical OSINT research, digital forensics learning, and cybersecurity skill development**.

---

## Features

### Core Correlation Engine
- Username normalization & similarity scoring
- Cross-platform presence comparison
- Stylometric writing analysis (linguistic fingerprinting)
- Confidence-weighted scoring system (0–100%)

### Platform Support
- Reddit
- Twitter / X
- Instagram
- Facebook
- Google (basic footprint)

### Image Matching (Optional)
- Face similarity comparison across profile images
- Designed for **catfishing detection research**
- Images are processed **in-memory only**
- No image storage or persistence

### Output
- Human-readable CLI output
- Optional JSON export for automation or further analysis

---

## Correlation Levels

PersonaFuse currently operates at **Level 2**:

| Level | Description |
|-----|------------|
| Level 1 | Username & platform presence only |
| **Level 2** | Username + platform + stylometry + optional face matching |
| Level 3 | (Planned) Behavioral, network, and metadata correlation |

---

## Installation

### Requirements
- Python **3.9 – 3.11** (recommended)
- pip
- Git

> ⚠️ **Important:**  
> The `face_recognition` dependency does **not reliably support Python 3.12+ / 3.13 on Windows**.  
> Image matching is optional and will gracefully disable if unavailable.

---

### Clone the Repository

```bash
git clone https://github.com/ArnoSXE/personafuse.git
cd personafuse
