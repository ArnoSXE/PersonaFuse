import requests
import numpy as np
import face_recognition
from io import BytesIO
from PIL import Image

def _image_from_url(url, timeout=8):
    r = requests.get(url, timeout=timeout)
    r.raise_for_status()
    img = Image.open(BytesIO(r.content)).convert("RGB")
    return np.asarray(img)

def extract_embeddings(image_urls, limit=5):
    embeddings = []

    for url in image_urls[:limit]:
        try:
            img_np = _image_from_url(url)
            faces = face_recognition.face_encodings(img_np)

            for f in faces:
                embeddings.append(f)

            # explicit memory cleanup
            del img_np
            del faces

        except Exception:
            continue

    return embeddings

def compare_faces(urls_user1, urls_user2):
    emb1 = extract_embeddings(urls_user1)
    emb2 = extract_embeddings(urls_user2)

    if not emb1 or not emb2:
        return {"available": False, "reason": "No faces detected"}

    scores = []
    for e1 in emb1:
        for e2 in emb2:
            dist = np.linalg.norm(e1 - e2)
            scores.append(max(0, 1 - dist))

    avg = float(np.mean(scores))
    score = int(round(avg * 100))

    if score >= 85:
        assessment = "Very likely same person"
    elif score >= 70:
        assessment = "Likely same person"
    elif score >= 50:
        assessment = "Possible match"
    else:
        assessment = "Unlikely match"

    return {
        "available": True,
        "faces_compared": len(scores),
        "image_similarity": score,
        "assessment": assessment
    }
