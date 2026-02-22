# BitStream
A pro-grade visual data storage tool that encodes files into bit-perfect, lossless FFV1 videos. Features a custom neon-cyberpunk dashboard, high-density RGB encoding, and steganography to hide data inside normal videos. Perfect for visual archival, air-gapped transfer, and experimental cloud backups.

 ### **🧠 Key Features**

*   📸 **Lossless FFV1 Integrity:** Uses the professional-grade FFV1 codec and AVI container to ensure every single bit is recovered exactly, preventing the corruption common in standard video compression.
*   🕵️ **Steganographic Tunneling:** Hide private files inside a "cover" video (like an anime clip or a lecture). To the naked eye, it looks like a normal video, but the software can extract the hidden payload.
*   🔄 **Dynamic UI Dashboard:** A sketch-accurate interface featuring a circular data-flow diagram between "Files" and "Video" with neon cyan and blue accents.
*   🧽 **Auto-Sort Engine:** Automatically categorizes extracted data into subfolders (Images, Docs, Programs, etc.) based on file extensions after decoding.
*   ⚡ **High-Density Scaling:** Supports custom resolutions from 256x256 up to 1080p allowing for massive data throughput—reaching theoretical speeds of over 1 GB/sec at extreme settings.

---
### **🛠️ Hardware & Software Stack**

| Component | Recommendation |
| :--- | :--- |
| **OS** | Windows 10/11 (Optimized), macOS, or Linux |
| **Python** | 3.10+ |
| **Libraries** | OpenCV, NumPy, CustomTkinter, tqdm |
| **Storage** | Sufficient space for uncompressed lossless AVI output |
---
**Core Dependencies:**
*   **OpenCV:** Handles pixel-to-frame transformations and codec management.
*   **NumPy:** Powers high-speed binary bitstream operations.
*   **CustomTkinter:** Provides the modern, hardware-accelerated UI components.
---

---

## **🛠️ Installation**

Ensure you have **Python 3.10+** installed. 

1.  **Clone and Install**
```bash
git clone https://github.com/mehuljain866/BitStream.git
cd BitStream
pip install -r requirements.txt
```
**or** download the .py files from the repo and put them in the same folder

---

## **📁 Required Folder Structure**

The application expects the following directory structure to function correctly:

```text
BitStream/
├── main.py                # Frontend UI
├── index.py               # Backend Engine
├── settings.json          # User configurations
├── input/
│   └── folder_to_encode/  # Drop files/folders here
├── cover_video/           # Store cover videos for steganography
└── output/
    ├── encoded_videos/    # Rendered .avi files
    └── extracted_files/   # Restored data after decoding
```

---
## **📖 How to Use**

### **1. Encoding (Files → Video)**
*   Click the **"Files"** label on the left to upload individual files or an entire folder. This copies your data into the local input directory.
*   Click the **top "convert" button** to begin the encoding process.
*   The application will compress your data into a ZIP archive and render it as a lossless AVI video.

### **2. Decoding (Video → Files)**
*   Click the **bottom "convert" button**.
*   Select an encoded `.avi` video from your computer.
*   The software will read the pixel data and reconstruct your original files in the `output/extracted_files/` folder.

### **3. Steganography Mode**
*   Open the **Settings** (gear icon in the top-left) and toggle **Steganography Mode** ON.
*   An **"Upload Cover Video"** button will appear. Use this to select the video you want to hide your data inside.
*   When you encode, BitStream will use Least Significant Bit (LSB) embedding to hide your data within the cover video's frames.

### **4. Settings**
*   **Resolution:** Higher resolutions significantly increase the amount of data stored per frame but require more processing power.
*   **Auto-Sort:** When enabled, extracted files are automatically organized by type.

---

### **💡 Recommendations**
*   **Compression First:** Always ZIP or 7z your folders *before* encoding to minimize the number of video frames required.
*   **Resolution Balance:** Use 512x512 for a good balance between data density and encoding speed.

*   ### **🧾 License**
This project is released under the **MIT License** for code and **Creative Commons BY-NC 4.0** for documentation.
**TL;DR:** Use it freely, modify it, but **don’t sell it without credit or permission**.

---

### **👋 Acknowledgments**
*   Special thanks to the open-source community for the FFV1 codec implementation.

---

### **📣 Author**
**Mehul Jain** — [GitHub Profile](https://github.com/mehuljain866)
*JEE Aspirant • Tinkerer • Tech Humanist*
