<!DOCTYPE html>
<html lang="th">
<head>
    <meta charset="utf-8">
    <title>Target Mania</title>
    <!-- ใช้ CDN สำรองที่เสถียรที่สุดเพื่อตัดปัญหาเรื่องการหาไฟล์ pythons.js ในเครื่องไม่เจอ -->
    <script src="https://jsdelivr.net"></script>
</head>
<body style="margin:0; background-color:black; color:lime; display:flex; flex-direction:column; justify-content:center; align-items:center; height:100vh; font-family:monospace; text-align:center;">
    
    <div id="status">⏳ กำลังเชื่อมต่อเครื่องยนต์เกม...</div>
    <div id="progress" style="display:none; color:cyan; margin-top:10px;">📦 กำลังโหลดไฟล์เกม (setup.tar.gz)...</div>
    <canvas id="canvas" style="display:none;"></canvas>

    <script>
        const status = document.getElementById('status');
        const progress = document.getElementById('progress');
        const canvas = document.getElementById('canvas');

        // ฟังก์ชันตรวจสอบและรันเกม
        async function initGame() {
            // เช็คว่าเครื่องยนต์โหลดมาหรือยัง
            if (window.AsyncPython) {
                status.style.display = "none";
                progress.style.display = "block";
                try {
                    // รันไฟล์ setup.tar.gz จากหน้าแรกของ GitHub
                    await window.AsyncPython.run("canvas", "setup.tar.gz");
                    progress.style.display = "none";
                    canvas.style.display = "block";
                } catch (e) {
                    progress.innerHTML = "❌ ไม่พบไฟล์ setup.tar.gz หรือไฟล์เสีย";
                    console.error(e);
                }
            } else {
                status.innerHTML = "❌ เครื่องยนต์ไม่ตอบสนอง (Engine Timeout)<br>กรุณากด Ctrl + F5";
            }
        }

        // เริ่มต้นหลังจากโหลดหน้าเว็บเสร็จ 2 วินาที
        window.addEventListener("load", () => {
            setTimeout(initGame, 2000);
        });
    </script>
</body>
</html>
