from fastapi import FastAPI
from fastapi.responses import JSONResponse

app = FastAPI()


@app.get("/", response_class=JSONResponse)
async def get_main_info():
    return {
        "message": "ยินดีต้อนรับสู่ SWC Admin API Gateway!",
        "endpoints": {
            "/api/register": "ลงทะเบียนผู้ดูแลระบบใหม่",
            "/api/login": "เข้าสู่ระบบสำหรับผู้ดูแลระบบที่มีอยู่แล้ว",
            "/api/request-password-reset": "ขอลิงก์รีเซ็ตรหัสผ่าน",
            "/api/reset-password": "รีเซ็ตรหัสผ่านโดยใช้โทเค็น",
        },
        "note": "โปรดดูเอกสารประกอบสำหรับรายละเอียดเพิ่มเติมเกี่ยวกับวิธีการใช้ API เหล่านี้.",
    }


# สามารถรันไฟล์นี้โดยตรงเพื่อทดสอบ
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
