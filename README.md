

# ChaiMaker Pro

**ChaiMaker Pro** is a creative and interactive **Streamlit web app** that lets users design their own chai recipe, get a unique AI-generated name, upload a photo, and download or share the recipe. It’s a fun project combining UI/UX, personalization, and real-time interaction — ideal for tea lovers and developers alike.

---

## 🚀 Features

* **Custom Chai Builder** – Select tea type, milk, sweetness, spices, strength, and boil time
* **AI Chai Name Generator** – Smart naming based on your ingredient choices
* **Image Upload** – Add and preview your chai image
* **Audio Effect** – Chai boiling sound plays on submission
* **Download Recipe** – Export your custom chai as a `.txt` file
* **Upload & Preview Recipes** – Share and open `.txt` recipe files
* **Rotating Tea Images** – JS-based image carousel every few seconds
* **Background Video** – Boiling chai background for immersive effect
* **Dark-Themed Styling** – Designed for modern, eye-comfortable UI

---

## 🧰 Tech Stack

* **Streamlit** – Core app framework
* **Python** – Logic, state, and file handling
* **HTML + CSS** – Background video and custom styling
* **JavaScript** – Rotating image logic (within Streamlit HTML block)

---

## 📁 Folder Structure

```
chaimaker-pro/
├── chaimaker_pro.py         # Main Streamlit app
├── README.md                # Project documentation
├── /screenshots             # App preview images (optional)
```

---

## 🖼️ Preview




├── <img width="1846" height="1044" alt="Screenshot 2025-07-10 020710" src="https://github.com/user-attachments/assets/dc0ff7e1-3359-4d37-a2e4-98774c6fccac" />

├── <img width="1852" height="991" alt="Screenshot 2025-07-10 020903" src="https://github.com/user-attachments/assets/a35e0bec-391c-41f2-9631-4bc370592c33" />

├── <img width="1556" height="1015" alt="Screenshot 2025-07-10 021003" src="https://github.com/user-attachments/assets/c92141e6-849d-4fdb-82fd-f08547af8055" />




Open in your browser at:

---

## 🌐 Deploy to Streamlit Cloud

1. Push this repo to GitHub
2. Go to [https://streamlit.io/cloud](https://streamlit.io/cloud)
3. Click **"Deploy an app"**
4. Choose your repo and set **`chaimaker_pro.py`** as the main file
5. Click **Deploy**

---

## ⚙️ Customization

| Feature          | How to Customize                     |
| ---------------- | ------------------------------------ |
| Background video | Replace video URL in HTML section    |
| Chai name logic  | Update `generate_chai_name()`        |
| Boiling sound    | Use a different `.mp3` URL           |
| Image rotation   | Modify JS array in `components.html` |

---

## 👤 Project By

### **Naman Agrawal**

[🔗 LinkedIn Profile](https://www.linkedin.com/in/naman-agrawal-8671aa27b/)



