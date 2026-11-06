# Đặc tả sản phẩm / quy trình chốt

| Bước | Trạng thái | Đầu ra | Điều kiện chuyển |
|---|---|---|---|
| 1. Nhập | `INTAKE` | Brief, niche, name mode, mood, locale | Có brief tối thiểu |
| 2. Chốt tên nếu cần | `AWAITING_NAME_SELECTION` | List tên đề xuất và cảnh báo clearance | Người dùng xác nhận tên |
| 3. Tạo ảnh demo | `PREVIEWS_GENERATING` | 10 ảnh concept nhận diện khác nhau mặc định, tối đa 20 | Tất cả preview có file hợp lệ |
| 4. Chọn concept | `AWAITING_USER_SELECTION` | Gallery, ảnh riêng, chọn/mix/sửa | Người dùng chọn >=1 concept |
| 5. Chốt asset types | `AWAITING_OUTPUT_SPEC` | Spec các file riêng do khách yêu cầu | Khách duyệt kích thước, loại ảnh, định dạng |
| 6. Sinh thành phẩm | `PRODUCTION` | Tệp brand riêng theo spec, không mặc định 6 | Engine đã tạo thật đủ file |
| 7. QA | `REVIEW_REQUIRED` | Kết quả kiểm tra máy; kết quả thẩm mỹ chờ duyệt | Tất cả technical pass + user approved |
| 8. Giao hàng | `COMPLETE` | ZIP + manifest + thumbnails + guide | Có file thực, đúng spec, chốt đã duyệt |

Bước 3: concept phải có logo/symbol, tên (khi đã có), màu, typography/visual system; tạo một ảnh/ý tưởng. Tránh ảnh động vật/cảnh nền đơn thuần không mang nhận diện. Bước 5: tùy ý profile: `CUSTOM` mặc định, `REFERENCE_MATCH`, `REFERENCE_6` optional, `YOUTUBE_BASIC` optional. Số lượng ảnh thành phẩm phụ thuộc asset spec; người dùng có thể chọn 1, 2, 6, 8 v.v. Nếu chọn nhiều concept (ví dụ 03 và 09), hỗ trợ xuất bộ asset riêng của từng concept.

Không dùng 'giai đoạn 10 ảnh' làm synonym 'đầu ra 6 ảnh'. Không dùng công việc chờ con người là 'hoàn tất'. Không tuyên bố tác vụ chạy nền nếu không có job queue thực sự. Preview chỉ dùng chế độ chi phí thấp, đặt watermark 'Preview' nếu phù hợp; tệp đầy đủ chỉ chạy sau khi duyệt. Tình trạng tất cả worker và chi phí phải được báo thực. Khi đa ngách, AI tự đề xuất palette/logo riêng, tên người dùng cung cấp là text chính xác (Unicode). Cần rights-check uploads và cảnh báo không giả làm nhãn hàng khác.

## Website thương mại
Wizard 4 trang: 1) Tên/ngách/ảnh mẫu. 2) 10-20 cards + progress, compare, select, regenerate, reference upload. 3) Build assets (preset hoặc custom rows với số px, filetype, transparency, safezone). 4) Production / per-file QA / download ZIP. Có tính cost estimate trước các lần gọi engine; rate limits; authentication; signed URLs; billing logs; safe prompts; file scanning, retention controls; i18n. Khách kiểm tra và chọn, agent không tự duyệt hộ.

## QA không thể giả
Máy: dimensions, format, alpha, file integrity, count, name consistency dựa trên metadata. Con người: chính tả rendered trong ảnh, trùng lặp style, cảm giác thương hiệu, IP rights. Nếu không nhìn ảnh, không được tuyên bố thẩm mỹ PASS.
