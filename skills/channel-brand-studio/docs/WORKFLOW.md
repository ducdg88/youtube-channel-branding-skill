# Đặc tả sản phẩm / quy trình chốt

| Bước | Lệnh `scripts/studio.py` | Trạng thái sau lệnh | Điều kiện chuyển |
|---|---|---|---|
| 1. Nhập | `init` | `PREVIEWS_PENDING` (chưa có tên: `AWAITING_NAME_SELECTION`) | Có brief tối thiểu |
| 2. Chốt tên nếu cần | `set-name` | `PREVIEWS_PENDING` | Người dùng xác nhận tên; chưa có tên thì `check-previews` và `select` bị chặn |
| 3. Kiểm ảnh demo | `check-previews` | `AWAITING_USER_SELECTION` (thiếu, lỗi: `PREVIEWS_INCOMPLETE`) | Đủ 10 (1 đến 20) ảnh concept hợp lệ, không trùng |
| 4. Chọn concept | `select` | `AWAITING_OUTPUT_SPEC` | Người dùng chọn ít nhất 1 concept |
| 5. Chốt asset types | `lock-spec` | `PRODUCTION` | Khách duyệt danh sách file, kích thước, định dạng |
| 6. Kiểm thành phẩm | `check-final` | `REVIEW_REQUIRED` (lỗi: `PRODUCTION_INCOMPLETE`) | Mọi file đúng spec; ghi kích thước và sha256 |
| 7. Duyệt bằng mắt | `approve-final --confirmed` | `COMPLETE` | Khách xem và đồng ý; file không đổi so với lúc kiểm |
| 8. Giao hàng | `bundle` | `COMPLETE`, có `deliverables.zip` | ZIP gồm file, `brand.lock.json`, `output_spec.lock.json`, `reports/final_qa.json`, `manifest.json` |

Chọn lại concept, chốt lại spec, kiểm lại ảnh demo hay chạy lại `check-final` đều xoá lần duyệt cũ: phải `approve-final` lại trước khi `bundle`.

Bước 3: concept phải có logo/symbol, tên (khi đã có), màu, typography/visual system; tạo một ảnh/ý tưởng. Tránh ảnh động vật/cảnh nền đơn thuần không mang nhận diện. Bước 5: tùy ý profile: `CUSTOM` mặc định, `REFERENCE_MATCH`, `REFERENCE_6` optional, `YOUTUBE_BASIC` optional. Số lượng ảnh thành phẩm phụ thuộc asset spec; người dùng có thể chọn 1, 2, 6, 8 v.v. Nếu chọn nhiều concept (ví dụ 03 và 09), hỗ trợ xuất bộ asset riêng của từng concept.

Không dùng 'giai đoạn 10 ảnh' làm synonym 'đầu ra 6 ảnh'. Không dùng công việc chờ con người là 'hoàn tất'. Không tuyên bố tác vụ chạy nền nếu không có job queue thực sự. Preview chỉ dùng chế độ chi phí thấp, đặt watermark 'Preview' nếu phù hợp; tệp đầy đủ chỉ chạy sau khi duyệt. Tình trạng tất cả worker và chi phí phải được báo thực. Khi đa ngách, AI tự đề xuất palette/logo riêng, tên người dùng cung cấp là text chính xác (Unicode). Cần rights-check uploads và cảnh báo không giả làm nhãn hàng khác.

## Website thương mại
Wizard 4 trang: 1) Tên/ngách/ảnh mẫu. 2) 10-20 cards + progress, compare, select, regenerate, reference upload. 3) Build assets (preset hoặc custom rows với số px, filetype, transparency, safezone). 4) Production / per-file QA / download ZIP. Có tính cost estimate trước các lần gọi engine; rate limits; authentication; signed URLs; billing logs; safe prompts; file scanning, retention controls; i18n. Khách kiểm tra và chọn, agent không tự duyệt hộ.

## QA không thể giả
Máy: dimensions, format, alpha, file integrity, count, name consistency dựa trên metadata. Con người: chính tả rendered trong ảnh, trùng lặp style, cảm giác thương hiệu, IP rights. Nếu không nhìn ảnh, không được tuyên bố thẩm mỹ PASS.
