import tkinter as tk
from tkinter import messagebox
import threading
import requests
import time
import base64

# هنا ضع صورة الباس64 الخاصة بك بين علامات الثلاثية:
BASE64_IMAGE = '''
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
'''

# الرابط الصحيح لواجهة الـ API لديك
API_URL = "https://jafgh.pythonanywhere.com/predict"


def activate_server():
    """
    دالة يتم تشغيلها عند الضغط على زر تفعيل السيرفر.
    تُرسل الصورة بصيغة Base64 إلى API، تقيس زمن الاستجابة، ثم تعرض النتائج على الواجهة.
    """
    def task():
        try:
            # تحديث الحالة أثناء المعالجة
            status_label.config(text="جاري الاتصال بالسيرفر...", fg="blue")

            # إعداد البيانات بصيغة JSON
            payload = {"image": BASE64_IMAGE}

            # قياس زمن المعالجة
            t0 = time.time()
            response = requests.post(API_URL, json=payload)
            elapsed_ms = (time.time() - t0) * 1000

            # تحليل الاستجابة
            if response.status_code == 200:
                try:
                    data = response.json()
                    message = f"تم بنجاح! الوقت المستغرق: {elapsed_ms:.1f} مللي ثانية"
                except ValueError:
                    message = f"استجابة غير JSON: {response.text}\nالوقت: {elapsed_ms:.1f} مللي ثانية"
            else:
                message = f"خطأ في السيرفر: {response.status_code}\nالوقت: {elapsed_ms:.1f} مللي ثانية"

            # عرض النتيجة على الواجهة
            status_label.config(text=message, fg="green" if response.status_code == 200 else "red")
            # يمكنك إلغاء تعليق السطر التالي إذا أردت نافذة إشعار منبثقة
            # messagebox.showinfo("نتيجة التفعيل", message)
        except Exception as e:
            status_label.config(text=f"حدث خطأ: {e}", fg="red")

    # تشغيل المهمة في Thread منفصل لمنع تجميد الواجهة
    threading.Thread(target=task, daemon=True).start()


# إنشاء واجهة Tkinter
root = tk.Tk()
root.title("واجهة تفعيل السيرفر")
root.geometry("400x200")

# زر واحد لتفعيل السيرفر
activate_button = tk.Button(
    root,
    text="تفعيل السيرفر",
    command=activate_server,
    font=("Arial", 14),
    width=20,
    height=2,
)
activate_button.pack(pady=20)

# لعرض حالة الاتصال ووقت الاستجابة
status_label = tk.Label(
    root,
    text="",
    font=("Arial", 12),
    wraplength=380,
    justify="center",
)
status_label.pack(pady=10)

# بدء الحلقة الرئيسية للواجهة
root.mainloop()
