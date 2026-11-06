# Ôn thi trắc nghiệm

Trang ôn tập trắc nghiệm cho AET102, HOD102, IPR và MLN131: xem câu hỏi kèm đáp án, làm đề 50 câu đảo thứ tự, chọn xong mới hiện đáp án.

Mở `index.html` trực tiếp hoặc qua GitHub Pages. Đáp án AET/HOD/IPR do AI giải và kiểm tra chéo; câu đánh dấu ⚠️ là chưa chắc chắn.

## Bật bảng xếp hạng (Firebase, miễn phí)

1. Vào https://console.firebase.google.com → **Add project** (tắt Google Analytics cho nhanh).
2. Trong project: **Build → Firestore Database → Create database** → chọn vùng `asia-southeast1` → **Start in production mode**.
3. Tab **Rules** của Firestore: dán nội dung file `firestore.rules` → **Publish**.
4. **Project settings (⚙️) → Your apps → biểu tượng `</>` (Web)** → đặt tên bất kỳ → Register. Copy đoạn `firebaseConfig = {...}`.
5. Dán vào `firebase-config.js`: `window.FIREBASE_CONFIG = { ...đoạn vừa copy... };` rồi commit.

Cấu hình web của Firebase là công khai theo thiết kế; dữ liệu được bảo vệ bằng `firestore.rules` (chỉ cho thêm điểm hợp lệ, không cho sửa/xóa).
