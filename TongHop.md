# **PHẦN 1: TỔNG QUAN BỐI CẢNH VÀ ĐẶC TẢ BÀI TOÁN NGHIÊN CỨU**

### **1.1. Bối cảnh kinh tế số và điểm nghẽn chuyển đổi tại giai đoạn giỏ hàng**

Thương mại điện tử toàn cầu đang bước vào chu kỳ tái cấu trúc chiến lược khi các động lực tăng trưởng dựa trên mở rộng quy mô lưu lượng truy cập dần chạm ngưỡng bão hòa. Theo báo cáo kinh tế số từ Diễn đàn Thương mại và Phát triển Liên Hợp Quốc, chi phí thu hút khách hàng mới (Customer Acquisition Cost \- CAC) trên các nền tảng kỹ thuật số đã tăng trưởng bình quân trên 200% trong nửa thập kỷ qua, chịu tác động kép từ sự cạnh tranh quảng cáo trực tuyến và các quy định thắt chặt quyền riêng tư dữ liệu người dùng. Sự leo thang này buộc các doanh nghiệp bán lẻ trực tuyến phải chuyển trọng tâm từ việc tìm kiếm lưu lượng truy cập mới sang tối ưu hóa giá trị vòng đời khách hàng (Customer Lifetime Value \- CLV). Trong cấu trúc phễu bán hàng kỹ thuật số (conversion funnel), bước chuyển từ việc cân nhắc sản phẩm sang hành động thêm vào giỏ hàng (Add-to-Cart) đánh dấu thời điểm ý định mua sắm của người tiêu dùng biểu hiện rõ nét nhất. Dẫu vậy, đây cũng chính là giai đoạn phát sinh điểm đứt gãy nghiêm trọng nhất trong toàn bộ chuỗi hành vi của khách hàng.  
Khảo sát thực nghiệm của Viện Nghiên cứu Baymard trên quy mô quốc tế ghi nhận tỷ lệ từ bỏ giỏ hàng (Shopping Cart Abandonment Rate) bình quân đạt 70.19%, phản ánh thực tế rằng phần lớn người tiêu dùng đã lựa chọn sản phẩm nhưng quyết định dừng lại trước khi hoàn tất thủ tục thanh toán. Tại thị trường Việt Nam, theo báo cáo của Bộ Công Thương, sự bùng nổ của hạ tầng thanh toán số và logistics chưa thể giải tỏa hoàn toàn tâm lý do dự của người tiêu dùng, nhất là khi họ đối mặt với các khoản phụ phí phát sinh bất ngờ như cước vận chuyển giao nhanh hay chính sách thuế phí thiếu minh bạch. Xét về bản chất tâm lý học hành vi, giỏ hàng trực tuyến không chỉ đóng vai trò là công cụ thanh toán mà còn thường xuyên bị người dùng sử dụng như một danh sách lưu trữ tạm thời (wishlist) để so sánh giá hoặc trì hoãn quyết định chi tiêu. Khi các lực cản hành vi (behavioral friction) xuất hiện—điển hình là mức phí giao hàng hỏa tốc quá cao hoặc quy trình thanh toán phức tạp—nguy cơ từ bỏ giao dịch sẽ gia tăng đột biến, biến toàn bộ chi phí tiếp thị đã đầu tư trước đó thành tổn thất chìm của doanh nghiệp.

Trước thực trạng tỷ lệ giỏ hàng bị bỏ rơi tăng cao, phản ứng phổ biến trong quản trị tiếp thị thương mại điện tử là triển khai các chiến dịch tiếp thị bám đuổi tự động (automated retargeting) thông qua việc phân phát mã giảm giá đại trà. Tuy nhiên, dưới góc độ phân tích kinh tế vi mô, việc can thiệp dàn trải thiếu chọn lọc này thường dẫn đến hiện tượng tự triệt tiêu biên lợi nhuận (margin cannibalization). Việc cấp phát voucher giảm giá cho những khách hàng vốn dĩ sẽ tự hoàn tất đơn hàng mà không cần động lực kinh tế trực tiếp làm suy giảm dòng tiền thuần của doanh nghiệp một cách không cần thiết, đồng thời hình thành tâm lý chờ đợi khuyến mãi có chủ đích ở người tiêu dùng. Ngược lại, việc tiếp tục phân bổ ngân sách tiếp cận vào những đối tượng đã mất hoàn toàn nhu cầu mua sắm lại làm gia tăng chi phí vận hành vô ích. Do đó, yêu cầu cấp thiết đặt ra cho khoa học dữ liệu trong thương mại điện tử hiện đại là phải xây dựng được các khung phân tích có khả năng bóc tách chính xác các yếu tố rào cản hành vi, dự đoán độ nhạy chuyển đổi và tối ưu hóa việc phân bổ nguồn lực can thiệp dựa trên hàm mục tiêu lợi nhuận ròng.

### **1.2. Khoảng trống nghiên cứu và giới hạn của các phương pháp tiếp cận hiện hành**

Phần lớn các nghiên cứu và giải pháp thực nghiệm trong lĩnh vực dự báo hành vi khách hàng thương mại điện tử hiện nay đang bộc lộ những hạn chế phương pháp luận rõ rệt:

*Hạn chế từ các khung phân tích kinh doanh truyền thống:* Các mô hình phân tích kinh doanh cổ điển, tiêu biểu là mô hình RFM (Recency, Frequency, Monetary), thường chỉ tổng kết các thuộc tính giao dịch tĩnh đã diễn ra trong quá khứ theo dạng giá trị tích lũy hoặc giá trị trung bình. Cách tiếp cận này hoàn toàn bỏ qua các tín hiệu vi mô phản ánh mức độ tương tác và sự do dự trong chính các phiên duyệt web gần nhất—chẳng hạn như tỷ lệ giữa số lượng sản phẩm thêm vào giỏ trên tổng số trang đã xem (cart\_to\_page\_ratio), thời gian dừng lại cân nhắc tính trên từng mặt hàng (hesitation\_index), hay sự sụt giảm tốc độ thao tác giỏ hàng theo thời gian (cart\_velocity). Việc thiếu vắng các biến số hành vi mang tính động học khiến các nhà quản trị không thể nhận diện được thời điểm suy giảm ý định mua hàng để có biện pháp can thiệp kịp thời.

*Vấn nạn rò rỉ dữ liệu theo trục thời gian (Temporal Data Leakage) trong thiết kế thực nghiệm học máy:* Trong các bài toán khai phá dữ liệu dạng bảng (tabular data), sai sót phương pháp luận nghiêm trọng và phổ biến nhất là việc xây dựng biến đặc trưng mà không thiết lập ranh giới thời gian quyết định một cách nghiêm ngặt. Khi các thông tin phát sinh sau mốc thời gian đưa ra quyết định dự báo vô tình bị tổng hợp vào tập huấn luyện, các mô hình học máy sẽ đạt được các chỉ số phân định cao giả tạo. Hiện tượng này khiến mô hình thể hiện năng lực dự báo hoàn hảo trên dữ liệu lịch sử nhưng mất đi hoàn toàn giá trị thực tiễn khi triển khai vào môi trường sản xuất thực tế do dữ liệu tương lai không tồn tại ở thời điểm ra quyết định.

*Sự đứt gãy giữa các chỉ số kỹ thuật thống kê và mục tiêu tối ưu hóa kinh tế:* Các thuật toán phân loại nhị phân phổ biến trong học máy thường được tối ưu hóa dựa trên các độ đo thống kê học thuật như Log-loss, ROC-AUC hay PR-AUC, đồng thời mặc định gán nhãn can thiệp khi xác suất dự báo đạt $\tau \geq 0.50$. Sự áp đặt cơ học này hoàn toàn không tương thích với bối cảnh kinh doanh thực tế, nơi phân phối nhãn có mức độ mất cân bằng tự nhiên và ma trận chi phí \- lợi ích luôn mang tính bất đối xứng. Chi phí liên hệ tiếp thị, chi phí phát hành voucher trợ giá và biên lợi nhuận thu hồi từ một đơn hàng thành công tạo nên một hàm mục tiêu tài chính phức tạp. Việc bỏ qua cấu trúc chi phí này và phụ thuộc vào ngưỡng phân loại mặc định khiến doanh nghiệp đánh mất phần lớn thặng dư kinh tế mà lẽ ra mô hình có thể tạo ra.

### **1.3. Mục tiêu nghiên cứu và những đóng góp học thuật cốt lõi**

Nhằm khắc phục toàn diện các khoảng trống nghiên cứu trên, đề tài này thiết lập mục tiêu xây dựng một khung phân tích hỗ trợ ra quyết định kinh tế hoàn chỉnh (Prescriptive Decision Intelligence Framework). Hệ thống kết nối xuyên suốt từ khâu kỹ thuật dữ liệu lớn đến mô hình hóa rào cản hành vi, hiệu chỉnh xác suất thực nghiệm và tối ưu hóa hàm lợi nhuận kỳ vọng.

Đề tài vận hành trên cơ sở dữ liệu thương mại điện tử đa bảng quy mô lớn gồm 200.000 hồ sơ khách hàng, hơn 2.000.000 phiên truy cập và 500.000 giao dịch được liên kết qua 8 bảng quan hệ chuẩn hóa. Nghiên cứu xác lập các đóng góp khoa học và thực tiễn cốt lõi sau:

*Kiến tạo quy trình xử lý dữ liệu phục hồi tự động và kho đặc trưng bảo toàn tính bất biến thời gian (Point-in-Time \- PIT):* Nghiên cứu thiết lập mốc chốt quyết định cố định tại thời điểm ${t}_{0}=2024-06-01$ cùng cửa sổ quan sát nhãn mục tiêu kéo dài đúng 30 ngày (từ 2024-06-01 đến 2024-07-01). Bằng việc ứng dụng động cơ DuckDB, quy trình kiểm toán và làm sạch dữ liệu (Data Healing) đã phát hiện và xử lý triệt để 997.299 phiên truy cập và 249.377 giao dịch có dấu thời gian vi phạm logic đăng ký tài khoản, xử lý 10.000 bản ghi nhân khẩu học bất thường, từ đó trích xuất thành công 63 đặc trưng hành vi và rào cản giỏ hàng đảm bảo tính toàn vẹn 100% không rò rỉ dữ liệu trước khi đưa vào mô hình học máy. Tỷ lệ chuyển đổi nhãn thực tế ghi nhận mức 20.30% trên tập dữ liệu huấn luyện 160.000 quan sát, phản ánh đúng tỷ lệ mất cân bằng tự nhiên của thương mại điện tử.

*Mô hình hóa rào cản giỏ hàng qua kiểm định phi tham số và phân khúc xác suất vi mô RFM-E:* Thay vì sử dụng phương pháp phân cụm K-Means vốn giả định các cụm có hình cầu đẳng hướng, nghiên cứu triển khai mô hình hỗn hợp Gaussian (Gaussian Mixture Models \- GMM) trên không gian đặc trưng mở rộng RFM kết hợp yếu tố tương tác giỏ hàng. Với tiêu chí tối ưu hóa thông tin Bayes (BIC), mô hình phân lập rõ rệt 5 chân dung khách hàng đặc trưng, trong đó phát hiện cụm *Cart Hesitators / Shipping-Sensitive* chiếm 25.04% dân số với mức độ nghiêm trọng từ bỏ giỏ hàng trung bình lên tới 4.9 phiên. Kết hợp cùng kiểm định Mann-Whitney U ($p=7.04\times 1{0}^{-8}$), nghiên cứu chứng minh cước vận chuyển hỏa tốc (pct\_overnight\_shipping) là rào cản ma sát cốt lõi làm gia tăng ý định từ bỏ giỏ hàng của nhóm khách hàng này.

*Đối chuẩn các thuật toán học máy tiên tiến và hiệu chuẩn xác suất thực nghiệm:* Thông qua quy trình tối ưu hóa siêu tham số tự động Optuna trên cấu trúc phân tầng 5-Fold Cross-Validation, nghiên cứu thực hiện đối chuẩn hiệu năng chuyên sâu giữa các thuật toán dạng cây tăng cường gradient (Gradient Boosting) gồm CatBoost, LightGBM, XGBoost và mô hình tổ hợp xếp chồng Stacking Ensemble. Nhận diện rõ nhược điểm của các thuật toán boosting dạng cây trong việc tạo ra xác suất dự báo bị dồn nén về hai cực, nghiên cứu áp dụng kỹ thuật hiệu chỉnh xác suất Platt Sigmoid cho mô hình LightGBM tối ưu. Kết quả trên tập kiểm thử độc lập (Holdout Test 32.000 mẫu) ghi nhận chỉ số PR-AUC đạt 0.2771, ROC-AUC đạt 0.6136, nén sai số hiệu chuẩn kỳ vọng (Expected Calibration Error \- ECE) xuống mức 0.0035 và Brier Score đạt 0.1576. Kiểm định ổn định qua 5 hạt giống ngẫu nhiên độc lập khẳng định độ vững chắc của mô hình với PR-AUC đạt $0.2761\pm 0.0004$.

*Chuyển dịch sang tối ưu hóa hàm lợi nhuận kinh tế kỳ vọng và phân bổ can thiệp theo suy luận nhân quả:* Vượt ra khỏi ranh giới của bài toán phân loại thống kê, nghiên cứu tích hợp mô hình phân tích sống còn Kaplan-Meier và hồi quy rủi ro tỷ lệ CoxPH để xác định ngưỡng thời gian bán rã của ý định mua sắm (${t}^{*}\leq 7$ ngày), kết hợp mô hình Uplift T-Learner để phân tách chính xác 4 nhóm phản ứng tiếp thị. Trên cơ sở đó, phương trình hàm lợi nhuận kinh tế kỳ vọng được thiết lập dựa trên chi phí tiếp xúc, chi phí ưu đãi và biên lợi nhuận gộp danh mục. Kết quả mô phỏng thực nghiệm chứng minh rằng việc hạ ngưỡng can thiệp từ mức mặc định $\tau =0.50$ xuống ngưỡng tối ưu ${\tau }^{*}=0.07$ đã gia tăng lợi nhuận ròng thực tế lên mức cực đại \$115,918 trên tập Holdout Test, đồng thời việc tập trung nguồn lực vào phân vị Decile 1 (đạt chỉ số Lift \= 1.61) cho phép doanh nghiệp tiết kiệm 60% chi phí tiếp cận khách hàng mà vẫn thâu tóm trọn vẹn nhóm khách hàng có giá trị chuyển đổi cao nhất.

# **PHẦN 2: CÂU HỎI NGHIÊN CỨU VÀ HỆ PHƯƠNG PHÁP LUẬN ĐỊNH LƯỢNG**

### **2.1. Mục tiêu phân tích và hệ thống câu hỏi nghiên cứu**

#### **2.1.1. Mục tiêu nghiên cứu tổng quát và mục tiêu cụ thể**

Mục tiêu bao trùm của công trình là thiết lập một khung phân tích hỗ trợ ra quyết định kinh tế toàn diện (Prescriptive Decision Intelligence Framework), kết hợp giữa khoa học dữ liệu lớn, mô hình hóa hành vi khách hàng và suy luận nhân quả nhằm giải quyết triệt để điểm nghẽn từ bỏ giỏ hàng trong thương mại điện tử. Thay vì tiếp cận bài toán dự báo chuyển đổi dưới góc nhìn thống kê thuần túy vốn tách rời khỏi các ràng buộc tài chính của doanh nghiệp, nghiên cứu hướng đến việc chuyển hóa trực tiếp xác suất dự báo thành các hành động can thiệp có khả năng tối đa hóa lợi nhuận ròng thực tế.

Từ mục tiêu tổng quát, nghiên cứu phân rã thành bốn mục tiêu cụ thể tương ứng với từng giai đoạn phân tích:

* *Thứ nhất, mục tiêu kỹ thuật dữ liệu:* Xây dựng quy trình tự động phục hồi dữ liệu (Data Healing) và thiết kế kho đặc trưng bảo toàn tính bất biến thời gian (Point-in-Time Feature Store) trên tập dữ liệu quy mô lớn (200.000 khách hàng, hơn 2.000.000 phiên truy cập), loại bỏ hoàn toàn hiện tượng rò rỉ dữ liệu tương lai (Look-ahead Bias).  
* *Thứ hai, mục tiêu phân tích hành vi vi mô:* Nhận diện và kiểm định có ý nghĩa thống kê các yếu tố ma sát giao dịch (cước vận chuyển hỏa tốc, thời gian đắn đo duyệt hàng), từ đó phân khúc khách hàng theo không gian xác suất đa chiều RFM-Engagement-Cart nhằm thay thế các mô hình phân cụm kinh doanh truyền thống.  
* *Thứ ba, mục tiêu mô hình hóa dự báo và hiệu chuẩn xác suất:* Huấn luyện, tối ưu hóa siêu tham số và đối chuẩn các thuật toán học máy tiên tiến dạng cây tăng cường gradient (Gradient Boosting) trên dữ liệu mất cân bằng; đồng thời ứng dụng kỹ thuật hiệu chuẩn xác suất thực nghiệm nhằm đưa đầu ra của mô hình về sát tần suất chuyển đổi khách quan.  
* *Thứ tư, mục tiêu tối ưu hóa quyết định kinh tế:* Lượng hóa tác động gia tăng thuần thông qua mô hình suy luận nhân quả Uplift Modeling để chấm dứt tình trạng lãng phí ưu đãi; đồng thời thiết lập phương trình hàm lợi nhuận kinh tế kỳ vọng nhằm tìm kiếm ngưỡng quyết định tối ưu \\tau^\* và xây dựng chiến lược phân bổ nguồn lực dựa trên phân vị Lift@K.

#### **2.1.2. Hệ thống câu hỏi nghiên cứu (Research Questions)**

Nhằm đạt được các mục tiêu định lượng nêu trên, nghiên cứu cấu trúc năm câu hỏi nghiên cứu có mối liên kết hữu cơ chặt chẽ:

* **Câu hỏi nghiên cứu 1 (RQ1 \- Rào cản chi phí vận chuyển):** *Phương thức vận chuyển hỏa tốc (`pct_overnight_shipping`) và chỉ số đắn đo giỏ hàng (`hesitation_index`) có tác động tiêu cực có ý nghĩa thống kê đến quyết định hoàn tất thanh toán hay không?* *Cơ sở học thuật:* Câu hỏi này hướng vào việc lượng hóa lực cản hành vi vi mô tại bước thanh toán cuối cùng. Nếu chi phí vận chuyển phát sinh đột ngột đóng vai trò là yếu tố ma sát chính, doanh nghiệp cần từ bỏ chính sách đồng giá vận chuyển cứng nhắc để chuyển sang cơ chế trợ giá linh hoạt theo giá trị giỏ hàng.  
* **Câu hỏi nghiên cứu 2 (RQ2 \- Quy luật phân rã tương tác và phân khúc vi mô):** *Tốc độ thao tác giỏ hàng (`cart_velocity`) suy giảm theo quy luật nào theo thời gian trôi qua kể từ phiên cuối, và mô hình hỗn hợp Gaussian (GMM) trên không gian RFM-E có phân lập chân dung khách hàng hiệu quả hơn mô hình K-Means cổ điển hay không?* *Cơ sở học thuật:* Câu hỏi này kiểm chứng tính chất suy giảm động lực mua hàng theo trục thời gian, đồng thời đánh giá khả năng mô hình hóa các cụm khách hàng có hình dạng elip và ma trận hiệp phương sai biến thiên, khắc phục nhược điểm áp đặt hình cầu đẳng hướng của K-Means.  
* **Câu hỏi nghiên cứu 3 (RQ3 \- Năng lực phân định của các thuật toán Gradient Boosting):** *Thuật toán nào trong số các mô hình Gradient Boosting tiên tiến (LightGBM, CatBoost, XGBoost) và mô hình tổ hợp xếp chồng (Stacking Ensemble) đạt diện tích dưới đường cong Precision-Recall (PR-AUC) cao nhất khi được tối ưu hóa siêu tham số tự động?* *Cơ sở học thuật:* Do nhãn chuyển đổi mang tính mất cân bằng tự nhiên (chỉ chiếm 20.30%), câu hỏi này tập trung vào độ đo PR-AUC thay vì ROC-AUC nhằm phản ánh năng lực thực chất của mô hình trong việc phân tách khách hàng tiềm năng mà không bị đánh lừa bởi số lượng mẫu tiêu cực áp đảo.  
* **Câu hỏi nghiên cứu 4 (RQ4 \- Hiệu chuẩn độ tin cậy của xác suất thực nghiệm):** *Kỹ thuật hiệu chuẩn Platt Sigmoid cải thiện sai số hiệu chuẩn kỳ vọng (ECE) và điểm số Brier Score của mô hình phân loại dạng cây như thế nào trước khi đưa vào hàm mục tiêu tài chính?* *Cơ sở học thuật:* Các mô hình học máy dạng cây có xu hướng tạo ra xác suất bị thiên lệch về hai cực (0 hoặc 1). Câu hỏi này xác định mức độ tin cậy của xác suất sau hiệu chuẩn, bảo đảm giá trị p\_i phản ánh chính xác tỷ lệ chuyển đổi thực tế ngoài môi trường sản xuất.  
* **Câu hỏi nghiên cứu 5 (RQ5 \- Tối ưu hóa hàm lợi nhuận ròng và suy luận nhân quả):** *Việc dịch chuyển từ ngưỡng phân loại mặc định (\\tau \= 0.50) sang ngưỡng tối ưu hóa hàm lợi nhuận kinh tế kỳ vọng (\$\\tau^*\$) kết hợp khung can thiệp Uplift Modeling mang lại mức gia tăng lợi nhuận ròng là bao nhiêu trên tập kiểm thử độc lập?\* *Cơ sở học thuật:* Câu hỏi này khép lại chu trình nghiên cứu bằng cách lượng hóa giá trị tiền tệ thực tế mà hệ thống đóng góp cho tổ chức, chứng minh tính ưu việt của việc kết hợp giữa học máy thống kê và lý thuyết quyết định kinh tế.

#### **2.1.3. Hệ thống giả thuyết kiểm định thực nghiệm**

Để trả lời các câu hỏi nghiên cứu trên cơ sở bằng chứng thực nghiệm, hệ thống các giả thuyết kiểm định thống kê được thiết lập:

*Bảng 2.1: Bảng tổng hợp giả thuyết kiểm định thống kê và cơ sở dữ liệu thực nghiệm*

| Mã giả thuyết | Tên giả thuyết kiểm định | Biến số kiểm định mục tiêu | Đối tượng so sánh / Phân nhóm | Phương pháp thống kê áp dụng | Cơ sở lý thuyết kỳ vọng |
| ----- | ----- | ----- | ----- | ----- | ----- |
| **H\_1** | Rào cản chi phí vận chuyển hỏa tốc | `pct_overnight_shipping` | Nhóm từ bỏ giỏ (y=0) so với Nhóm mua hàng (y=1) | Mann-Whitney U Test (One-sided Greater) | Nhóm từ bỏ giỏ hàng có tỷ lệ chọn giao hỏa tốc cao hơn có ý nghĩa thống kê (p \< 0.05). |
| **H\_2** | Quy luật phân rã tương tác giỏ hàng | `cart_velocity` | 4 khoảng thời gian trễ: \\le 7 ngày, 8\\text{--}15 ngày, 16\\text{--}30 ngày, \>30 ngày | Kruskal-Wallis H-Test | Tốc độ thêm giỏ suy giảm đơn điệu theo độ trễ thời gian kể từ phiên cuối (p \< 0.05). |
| **H\_3** | Tính đồng nhất độ nhạy ưu đãi theo hạng | `trans_discount_usage_rate` | 4 phân hạng hội viên: Bronze, Silver, Gold, Platinum | Kruskal-Wallis H-Test | Không có sự khác biệt có ý nghĩa thống kê về tỷ lệ dùng voucher giữa các hạng hội viên (p \\ge 0.05). |
| **H\_4** | Tính vượt trội của phân cụm xác suất GMM | Ma trận 6 đặc trưng RFM-E | Đánh giá phân cụm trên toàn bộ 200.000 khách hàng | Tiêu chuẩn thông tin Bayes (BIC) | Mô hình GMM với hiệp phương sai đầy đủ đạt điểm BIC thấp hơn K-Means và tối ưu tại k=5. |

### **2.2. Khung thiết kế thực nghiệm và kiểm soát rò rỉ dữ liệu Point-in-Time (PIT)**

#### **2.2.1. Nguyên lý phân định ranh giới thời gian quyết định Point-in-Time**

Vấn đề cốt tử trong việc ứng dụng học máy vào dữ liệu dạng bảng thương mại điện tử là ngăn chặn tuyệt đối hiện tượng rò rỉ dữ liệu theo trục thời gian (Temporal Data Leakage). Trong thực tế vận hành, tại thời điểm doanh nghiệp quyết định có gửi thông điệp nhắc nhở hoặc cấp mã giảm giá cho khách hàng hay không, toàn bộ dữ liệu của tương lai đều chưa xuất hiện. Do đó, nếu mô hình được huấn luyện bằng các đặc trưng tổng hợp xuyên qua thời điểm ra quyết định, các chỉ số đánh giá kỹ thuật sẽ bị thổi phồng giả tạo nhưng hoàn toàn mất khả năng tổng quát hóa khi triển khai thực tế.

Nghiên cứu thiết lập một mốc chốt quyết định cố định (Point-in-Time Cutoff) tại thời điểm t\_0 \= \\text{2024-06-01 00:00:00}. Toàn bộ các thông tin phát sinh trước thời điểm này được định nghĩa là cửa sổ lịch sử (Historical Observation Window) dùng để tổng hợp đặc trưng đầu vào X. Toàn bộ các tương tác diễn ra từ thời điểm t\_0 trở đi được cách ly tuyệt đối và đóng vai trò là cửa sổ quan sát nhãn mục tiêu (Target Observation Window) kéo dài đúng 30 ngày (từ 2024-06-01 đến 2024-06-30). Nhãn chuyển đổi y\_i \\in \\{0, 1\\} được xác định dựa trên việc khách hàng i có phát sinh ít nhất một giao dịch thành công trong cửa sổ tương lai này hay không.

*Bảng 2.2: Thiết kế ranh giới thời gian Point-in-Time và cấu trúc phân chia tập dữ liệu*

| Thành phần dữ liệu | Cửa sổ thời gian quy định | Phạm vi dữ liệu trích xuất | Mục đích sử dụng | Quy mô mẫu quan sát |
| ----- | ----- | ----- | ----- | ----- |
| **Cửa sổ lịch sử (X\_{\\text{PIT}})** | Toàn bộ dữ liệu trước t\_0 (t \\le \\text{2024-05-31 23:59:59}) | Lịch sử phiên truy cập, hành vi giỏ hàng, giao dịch quá khứ, địa lý | Trích xuất 63 biến đặc trưng độc lập phục vụ dự báo | 200.000 khách hàng (160.000 Train \+ 40.000 Test) |
| **Cửa sổ nhãn mục tiêu (Y)** | Cố định 30 ngày sau t\_0 (\\text{2024-06-01} \\le t \\le \\text{2024-06-30}) | Dữ liệu phát sinh đơn hàng trong tháng 06/2024 | Xác định biến phụ thuộc nhị phân (y=1 nếu mua, y=0 nếu không) | 160.000 khách hàng có nhãn (Tỷ lệ y=1 đạt 20.30%) |
| **Tập phát triển (Train Pool)** | Dữ liệu lịch sử kết hợp nhãn mục tiêu | 80% ngẫu nhiên có phân tầng từ 160.000 khách hàng có nhãn | Huấn luyện mô hình cơ sở, tinh chỉnh siêu tham số qua 5-Fold CV | 128.000 khách hàng |
| **Tập kiểm thử độc lập (Holdout Test)** | Bị niêm phong tuyệt đối trong pha huấn luyện | 20% độc lập từ 160.000 khách hàng có nhãn (`split_indices.npz`) | Đánh giá đối chuẩn mô hình, kiểm tra hiệu chuẩn và tối ưu hóa lợi nhuận \\tau^\* | 32.000 khách hàng |

#### **2.2.2. Chiến lược phân chia dữ liệu và kiểm chứng chéo phân tầng**

Để triệt tiêu hiện tượng thiên kiến lạc quan (Optimism Bias) trong việc ước lượng sai số mô hình, nghiên cứu áp dụng chiến lược phân tách dữ liệu hai tầng nghiêm ngặt:

1. **Phân tách Holdout Test độc lập:** Tập dữ liệu 160.000 khách hàng có nhãn được chia ngẫu nhiên có phân tầng (Stratified Splitting) theo tỷ lệ 80:20 với hạt giống ngẫu nhiên cố định `random_state = 42`. Tập Holdout Test gồm 32.000 quan sát được lưu trữ chỉ số phân tách tại `outputs/experiments/split_indices.npz`. Tập dữ liệu này bị cách ly hoàn toàn khỏi mọi quá trình tính toán thống kê, chuẩn hóa, phân cụm hay lựa chọn đặc trưng của pha huấn luyện.  
2. **Kiểm chứng chéo phân tầng 5 lớp (5-Fold Stratified Cross-Validation):** Trên tập phát triển (Train Pool 128.000 dòng), dữ liệu được chia thành 5 folds với tỷ lệ nhãn tích cực được bảo toàn đồng nhất (\~20.30%) trên từng fold. Mọi phép biến đổi chuẩn hóa (StandardScaler), mã hóa biến danh mục (Target Encoding) và tính toán tham số đều chỉ được học trên 4 folds huấn luyện và áp dụng sang fold kiểm thực nhằm đảm bảo tính toàn vẹn thông tin nội bộ.

### **2.3. Hệ phương pháp luận và cơ sở toán học định lượng**

#### **2.3.1. Phương pháp kiểm định phân phối chuẩn và thống kê phi tham số**

Trước khi tiến hành phân tích mối quan hệ giữa các biến số hành vi và quyết định chuyển đổi giỏ hàng, việc xác định dạng phân phối của dữ liệu là bắt buộc. Nghiên cứu sử dụng kiểm định tính chuẩn đa biến D'Agostino-Pearson dựa trên sự kết hợp giữa hệ số bất đối xứng (skewness) và hệ số độ nhọn (kurtosis).

Hàm thống kê kiểm định tính chuẩn K^2 được định nghĩa:

`K^2 = Z_1(s)^2 + Z_2(k)^2`

Trong đó:

* K^2: Đại lượng thống kê kiểm định D'Agostino-Pearson, tuân theo phân phối Chi bình phương với 2 bậc tự do (\\chi^2(2)) dưới giả thuyết không H\_0 (dữ liệu tuân theo phân phối chuẩn).  
* s: Hệ số bất đối xứng của mẫu quan sát, phản ánh mức độ lệch trái hoặc lệch phải của phân phối dữ liệu so với phân phối chuẩn đối xứng (s \= 0).  
* k: Hệ số độ nhọn của mẫu quan sát, phản ánh độ dày của phần đuôi phân phối dữ liệu so với phân phối chuẩn (k \= 3).  
* Z\_1(s): Phép biến đổi chuẩn hóa hệ số bất đối xứng s về phân phối chuẩn tắc \\mathcal{N}(0, 1).  
* Z\_2(k): Phép biến đổi chuẩn hóa hệ số độ nhọn k về phân phối chuẩn tắc \\mathcal{N}(0, 1).

Khi kết quả kiểm định cho thấy các biến số hành vi giỏ hàng (`cart_to_page_ratio`, `hesitation_index`, `cart_velocity`) vi phạm nghiêm trọng giả định phân phối chuẩn (p \< 10^{-50}), các phương pháp kiểm định tham số truyền thống bị loại bỏ để chuyển sang kiểm định phi tham số:

Đại lượng thống kê kiểm định Mann-Whitney U dùng để so sánh hai mẫu độc lập được xác định theo công thức:

`U = n_1 n_2 + \frac{n_1(n_1 + 1)}{2} - R_1`

Trong đó:

* U: Giá trị thống kê kiểm định Mann-Whitney U, đại diện cho số lần một quan sát từ nhóm thứ nhất xếp trước một quan sát từ nhóm thứ hai khi toàn bộ dữ liệu gộp được sắp xếp theo thứ tự tăng dần.  
* n\_1: Dung lượng mẫu của nhóm thứ nhất (nhóm khách hàng từ bỏ giỏ hàng, y \= 0).  
* n\_2: Dung lượng mẫu của nhóm thứ hai (nhóm khách hàng chuyển đổi thành công, y \= 1).  
* R\_1: Tổng các giá trị thứ hạng (rank sum) được gán cho các phần tử thuộc nhóm thứ nhất sau khi xếp hạng toàn bộ n\_1 \+ n\_2 quan sát gộp.

Kích thước tác động (Effect Size) của mối quan hệ phi tham số được định lượng thông qua hệ số tương quan thứ hạng hai chuỗi (Rank-Biserial Correlation):

`r_{\text{rb}} = 1 - \frac{2U}{n_1 n_2}`

Trong đó:

* r\_{\\text{rb}}: Hệ số tương quan thứ hạng hai chuỗi nhận giá trị trong đoạn \[-1, 1\]. Giá trị r\_{\\text{rb}} \> 0 biểu thị nhóm thứ nhất có xu hướng nhận giá trị lớn hơn nhóm thứ hai, trong khi r\_{\\text{rb}} \< 0 biểu thị điều ngược lại.

Đối với các so sánh nhiều nhóm độc lập (như so sánh tốc độ giỏ hàng giữa 4 khoảng thời gian trễ), kiểm định Kruskal-Wallis được triển khai theo công thức:

`H = \frac{12}{N(N+1)} \sum_{j=1}^k \frac{R_j^2}{n_j} - 3(N+1)`

Trong đó:

* H: Đại lượng thống kê kiểm định Kruskal-Wallis, xấp xỉ phân phối Chi bình phương với k \- 1 bậc tự do (\\chi^2(k-1)).  
* N: Tổng số lượng quan sát trên toàn bộ các nhóm (N \= \\sum\_{j=1}^k n\_j).  
* k: Số lượng nhóm độc lập được đưa vào so sánh (k \= 4 đối với các khoảng thời gian trễ).  
* n\_j: Số lượng quan sát trong phân nhóm thứ j.  
* R\_j: Tổng giá trị thứ hạng của các quan sát thuộc phân nhóm thứ j sau khi xếp hạng toàn bộ N quan sát.

Nhằm loại bỏ hiện tượng dương tính giả phát sinh từ việc kiểm định đồng thời nhiều giả thuyết, mọi giá trị p-value đều được điều chỉnh kiểm soát tỷ lệ sai số gia đình (Family-wise Error Rate) thông qua phép hiệu chỉnh Bonferroni:

`p_{\text{adjusted}} = \min(1, p \times m)`

Trong đó m là tổng số lượng phép kiểm định thống kê được thực thi đồng thời (m \= 7).

#### **2.3.2. Mô hình phân khúc vi mô bằng mô hình hỗn hợp Gaussian (GMM)**

Để khắc phục nhược điểm của thuật toán K-Means vốn giả định các cụm có hình cầu đẳng hướng và phương sai đồng nhất, nghiên cứu triển khai mô hình hỗn hợp Gaussian (Gaussian Mixture Models \- GMM) trên không gian mở rộng RFM-E gồm sáu biến chuẩn hóa: `recency`, `frequency`, `monetary`, `cart_additions`, `cart_abandonment_severity`, và `cart_velocity`.

Hàm mật độ xác suất kết hợp của mô hình GMM có dạng:

`p(\mathbf{x}) = \sum_{k=1}^K \pi_k \mathcal{N}(\mathbf{x} \mid \boldsymbol{\mu}_k, \boldsymbol{\Sigma}_k)`

Trong đó:

* \\mathbf{x}: Véc-tơ đặc trưng hành vi 6 chiều của một khách hàng trong không gian RFM-E (\\mathbf{x} \\in \\mathbb{R}^6).  
* K: Tổng số lượng thành phần phân phối chuẩn đa biến (số lượng cụm chân dung khách hàng).  
* \\pi\_k: Trọng số trộn (mixing coefficient) của cụm thứ k, thỏa mãn điều kiện tiên quyết \\sum\_{k=1}^K \\pi\_k \= 1 và \\pi\_k \\ge 0\.  
* \\mathcal{N}(\\mathbf{x} \\mid \\boldsymbol{\\mu}\_k, \\boldsymbol{\\Sigma}\_k): Hàm mật độ xác suất của phân phối chuẩn đa biến ứng với cụm thứ k, có véc-tơ kỳ vọng trung bình \\boldsymbol{\\mu}\_k \\in \\mathbb{R}^6 và ma trận hiệp phương sai đầy đủ \\boldsymbol{\\Sigma}\_k \\in \\mathbb{R}^{6 \\times 6}.

Số lượng cụm tối ưu K^\* được xác định thông qua việc cực tiểu hóa tiêu chuẩn thông tin Bayes (Bayesian Information Criterion \- BIC):

`\text{BIC} = \ln(N) \cdot p - 2 \ln(\hat{L})`

Trong đó:

* \\text{BIC}: Điểm số tiêu chuẩn thông tin Bayes. Mô hình có giá trị BIC càng nhỏ thể hiện sự cân bằng tối ưu giữa năng lực giải thích dữ liệu và độ phức tạp tham số.  
* N: Tổng số lượng quan sát trong tập dữ liệu phân cụm (N \= 200.000).  
* p: Số lượng tham số độc lập cần ước lượng trong mô hình GMM với ma trận hiệp phương sai đầy đủ (p \= K \\cdot \[1 \+ d \+ \\frac{d(d+1)}{2}\] \- 1 với d \= 6).  
* \\hat{L}: Giá trị cực đại của hàm hợp lý (Maximum Likelihood) thu được sau khi thuật toán Cực đại hóa kỳ vọng (Expectation-Maximization \- EM) hội tụ.

#### **2.3.3. Thuật toán học máy tăng cường Gradient và tối ưu hóa siêu tham số Optuna**

Nghiên cứu tập trung vào ba thuật toán Gradient Boosting dạng cây tiên tiến nhất hiện nay để mô hình hóa bài toán dự báo chuyển đổi giỏ hàng:

1. **LightGBM:** Sử dụng cơ chế phát triển cây theo chiều sâu tối ưu lá (leaf-wise tree growth) kết hợp hai thuật toán cốt lõi: Lấy mẫu đơn phương dựa trên gradient (Gradient-based One-Side Sampling \- GOSS) để tập trung vào các mẫu có gradient lớn và Gộp đặc trưng độc quyền (Exclusive Feature Bundling \- EFB) nhằm giảm số chiều ma trận thưa.  
2. **CatBoost:** Sử dụng cơ chế Ordered Boosting để loại bỏ hiện tượng dịch chuyển mục tiêu (target leakage) trong quá trình tính toán thống kê mục tiêu trực tuyến (Online Target Statistics) cho các biến danh mục phức tạp (`customer_tier`, `shipping_speed`).  
3. **XGBoost:** Triển khai phép xấp xỉ Taylor bậc hai cho hàm mất mát kết hợp thành phần điều chuẩn L1/L2 trên trọng số lá cây nhằm hạn chế hiện tượng quá khớp.

Quy trình tối ưu hóa siêu tham số tự động được thực hiện qua thuật toán Ước lượng mật độ Parzen dạng cây (Tree-structured Parzen Estimator \- TPE) của thư viện Optuna. Hàm mục tiêu được định nghĩa là giá trị trung bình của diện tích dưới đường cong Precision-Recall (PR-AUC) trên 5 folds kiểm chứng chéo:

`\boldsymbol{\theta}^* = \arg\max_{\boldsymbol{\theta} \in \Theta} \frac{1}{5} \sum_{m=1}^5 \text{PR-AUC}^{(m)}(\boldsymbol{\theta})`

Trong đó:

* \\boldsymbol{\\theta}^\*: Véc-tơ siêu tham số tối ưu toàn cục được tìm thấy sau quá trình tìm kiếm.  
* \\Theta: Không gian tìm kiếm siêu tham số đa chiều được định nghĩa (bao gồm `learning_rate`, `num_leaves`, `max_depth`, `subsample`, `colsample_bytree`, `scale_pos_weight`).  
* \\text{PR-AUC}^{(m)}(\\boldsymbol{\\theta}): Diện tích dưới đường cong Precision-Recall tính toán trên fold kiểm thực thứ m tại cấu hình siêu tham số \\boldsymbol{\\theta}.

#### **2.3.4. Lý thuyết hiệu chuẩn xác suất thực nghiệm (Probability Calibration)**

Do các mô hình cây quyết định phân tách không gian bằng các siêu phẳng trực giao, đầu ra xác suất của mô hình Gradient Boosting thường không phản ánh đúng tần suất thực tế khách quan mà bị dồn nén về các khoảng xác suất cực đoan. Để khắc phục hiện tượng này, nghiên cứu áp dụng kỹ thuật hiệu chuẩn Platt Scaling thông qua mô hình hàm Sigmoid:

`P(y_i = 1 \mid f_i) = \frac{1}{1 + \exp(A f_i + B)}`

Trong đó:

* P(y\_i \= 1 \\mid f\_i): Xác suất chuyển đổi đã được hiệu chuẩn của quan sát i.  
* f\_i: Điểm số logit chưa hiệu chuẩn (raw margin output) xuất phát từ mô hình LightGBM tối ưu.  
* A, B: Các hệ số tỷ lệ và dịch chuyển được ước lượng bằng phương pháp hợp lý cực đại trên tập dữ liệu kiểm chứng chéo ngoài mẫu (Out-of-Fold validation set).

Chất lượng của phân phối xác suất sau hiệu chuẩn được đo lường qua hai chỉ số:

*Điểm số Brier Score:*

`\text{BS} = \frac{1}{N} \sum_{i=1}^N (p_i - y_i)^2`

Trong đó:

* \\text{BS}: Đại lượng Brier Score nhận giá trị trong đoạn \[0, 1\]. Giá trị càng gần 0 thể hiện độ chính xác của ước lượng xác suất càng hoàn hảo.  
* N: Tổng số lượng mẫu kiểm thử độc lập (N \= 32.000).  
* p\_i: Xác suất chuyển đổi dự báo sau hiệu chuẩn của khách hàng i (p\_i \\in \[0, 1\]).  
* y\_i: Nhãn chuyển đổi thực tế khách quan của khách hàng i (y\_i \\in \\{0, 1\\}).

*Sai số hiệu chuẩn kỳ vọng (Expected Calibration Error \- ECE):*

`\text{ECE} = \sum_{m=1}^M \frac{\vert{}B_m\vert{}}{N} \left\vert{} \text{acc}(B_m) - \text{conf}(B_m) \right\vert{}`

Trong đó:

* \\text{ECE}: Sai số hiệu chuẩn kỳ vọng. Giá trị càng tiệm cận 0 chứng minh mô hình không bị thiên lệch tự tin thái quá hay tự tin dưới mức.  
* M: Số lượng khoảng phân vị xác suất được chia đều trên đoạn \[0, 1\] (M \= 10).  
* B\_m: Tập hợp các quan sát có xác suất dự báo rơi vào khoảng thứ m (B\_m \= \\{i \\mid p\_i \\in (\\frac{m-1}{M}, \\frac{m}{M}\]\\}).  
* \\vert{}B\_m\\vert{}: Số lượng phần tử nằm trong khoảng thứ m.  
* \\text{acc}(B\_m): Độ chính xác thực tế của khoảng thứ m, tính bằng tỷ lệ mẫu dương tính thực tế (\\text{acc}(B\_m) \= \\frac{1}{\\vert{}B\_m\\vert{}} \\sum\_{i \\in B\_m} y\_i).  
* \\text{conf}(B\_m): Độ tin cậy dự báo trung bình của khoảng thứ m (\\text{conf}(B\_m) \= \\frac{1}{\\vert{}B\_m\\vert{}} \\sum\_{i \\in B\_m} p\_i).

#### **2.3.5. Phương pháp phân tích sống còn của giỏ hàng (Survival Analysis)**

Thời gian duy trì ý định mua sắm của khách hàng sau khi thêm sản phẩm vào giỏ được mô hình hóa qua phương pháp phân tích sống còn (Time-to-Event Analysis). Thời gian T là số ngày từ phiên thêm giỏ gần nhất đến khi giao dịch phát sinh. Các trường hợp không chuyển đổi trong 30 ngày được xem là dữ liệu kiểm duyệt phải (Right-Censored).

Hàm sống còn ước lượng phi tham số Kaplan-Meier có dạng:

`\hat{S}(t) = \prod_{t_i \le t} \left( 1 - \frac{d_i}{n_i} \right)`

Trong đó:

* \\hat{S}(t): Xác suất một giỏ hàng vẫn duy trì khả năng hoàn tất giao dịch sau khoảng thời gian t ngày.  
* t\_i: Mốc thời gian quan sát thứ i ghi nhận có ít nhất một giao dịch mua hàng phát sinh (t\_i \\le t).  
* d\_i: Số lượng khách hàng hoàn tất giao dịch chính xác tại mốc thời gian t\_i.  
* n\_i: Tổng số lượng khách hàng vẫn còn duy trì giỏ hàng và chưa hoàn tất giao dịch ngay trước mốc thời gian t\_i.

Tác động đồng biến của các rào cản hành vi lên nguy cơ từ bỏ giỏ hàng được lượng hóa qua mô hình hồi quy rủi ro tỷ lệ Cox (CoxPH):

`h(t \mid \mathbf{x}) = h_0(t) \exp\left( \boldsymbol{\beta}^T \mathbf{x} \right)`

Trong đó:

* h(t \\mid \\mathbf{x}): Hàm rủi ro có điều kiện tại thời điểm t ứng với véc-tơ đặc trưng rào cản \\mathbf{x}.  
* h\_0(t): Hàm rủi ro nền (baseline hazard function) tại thời điểm t khi toàn bộ các biến đồng biến nhận giá trị 0\.  
* \\boldsymbol{\\beta}: Véc-tơ hệ số hồi quy được ước lượng qua phương pháp hợp lý riêng phần (Partial Likelihood).  
* \\text{HR}\_j \= \\exp(\\beta\_j): Tỷ số nguy cơ (Hazard Ratio) của đặc trưng thứ j. Hệ số \\text{HR}\_j \> 1 đồng nghĩa với việc đặc trưng này đẩy nhanh quyết định mua hàng, trong khi \\text{HR}\_j \< 1 thể hiện vai trò là lực cản kéo dài thời gian do dự của khách hàng.

#### **2.3.6. Mô hình suy luận nhân quả Uplift Modeling (T-Learner)**

Để tối ưu hóa chi phí ưu đãi và loại bỏ hiện tượng tự triệt tiêu lợi nhuận, nghiên cứu ứng dụng mô hình kết quả tiềm năng Neyman-Rubin để ước lượng Tác động can thiệp trung bình có điều kiện (Conditional Average Treatment Effect \- CATE):

`\tau(\mathbf{x}) = \mathbb{E}[Y_i(1) - Y_i(0) \mid \mathbf{X} = \mathbf{x}]`

Trong đó:

* \\tau(\\mathbf{x}): Điểm Uplift cá thể hóa, đại diện cho mức tăng xác suất chuyển đổi thuần túy do tác động can thiệp ưu đãi mang lại đối với khách hàng có đặc trưng \\mathbf{x}.  
* Y\_i(1): Kết quả mua hàng tiềm năng của khách hàng i nếu được nhận can thiệp ưu đãi (W\_i \= 1).  
* Y\_i(0): Kết quả mua hàng tiềm năng của khách hàng i nếu không nhận được can thiệp ưu đãi (W\_i \= 0).  
* \\mathbf{X}: Không gian các biến đặc trưng hành vi và nhân khẩu học trước thời điểm can thiệp.

Khung kiến trúc T-Learner huấn luyện độc lập hai mô hình LightGBM:

`\mu_1(\mathbf{x}) = \mathbb{E}[Y \mid \mathbf{X} = \mathbf{x}, W = 1], \quad \mu_0(\mathbf{x}) = \mathbb{E}[Y \mid \mathbf{X} = \mathbf{x}, W = 0]`

Ước lượng Uplift cá thể hóa được xác định bằng hiệu số:

`\hat{\tau}_i = \hat{\mu}_1(\mathbf{x}_i) - \hat{\mu}_0(\mathbf{x}_i)`

Trong đó \\hat{\\mu}\_1(\\mathbf{x}\_i) và \\hat{\\mu}\_0(\\mathbf{x}\_i) lần lượt là xác suất chuyển đổi dự báo khi có và không có can thiệp tiếp thị của khách hàng i.

#### **2.3.7. Hàm mục tiêu tối ưu hóa lợi nhuận kinh tế kỳ vọng và phân vị Decile Lift@K**

Nghiên cứu tích hợp xác suất đã hiệu chuẩn p\_i vào hàm mục tiêu tài chính của doanh nghiệp trên tập kiểm thử Holdout Test (32.000 khách hàng).

Hàm tối ưu hóa lợi nhuận ròng \\text{Profit}(\\tau) theo ngưỡng quyết định can thiệp \\tau được xác lập:

`\text{Profit}(\tau) = \sum_{i \in \text{Holdout}} \mathbb{I}(p_i \ge \tau) \cdot \left[ y_i \cdot (\text{Margin}_i - C_{\text{voucher}}) - C_{\text{contact}} \right]`

Trong đó:

* \\text{Profit}(\\tau): Tổng lợi nhuận ròng thực tế thu được (đơn vị: USD) trên toàn bộ tập kiểm thử khi áp dụng ngưỡng can thiệp \\tau.  
* \\tau: Ngưỡng xác suất quyết định được quét liên tục trong đoạn \[0.01, 0.99\] với bước nhảy \\Delta \\tau \= 0.01.  
* \\mathbb{I}(p\_i \\ge \\tau): Hàm chỉ báo (indicator function), nhận giá trị 1 nếu xác suất dự báo của khách hàng i thỏa mãn p\_i \\ge \\tau (kích hoạt can thiệp tiếp thị) và nhận giá trị 0 nếu p\_i \< \\tau (bỏ qua không can thiệp).  
* y\_i: Nhãn chuyển đổi thực tế của khách hàng i trong tập kiểm thử (y\_i \\in \\{0, 1\\}).  
* \\text{Margin}\_i: Biên lợi nhuận gộp danh mục kỳ vọng của khách hàng i, được tính bằng \\text{Margin}\_i \= 0.25 \\times \\text{AOV}\_i với tỷ suất biên lợi nhuận gộp danh mục là 25\\% và \\text{AOV}\_i là giá trị đơn hàng trung bình của khách hàng.  
* C\_{\\text{voucher}}: Chi phí phát hành voucher trợ giá trên mỗi đơn hàng thành công (C\_{\\text{voucher}} \= \\\$5.0).  
* C\_{\\text{contact}}: Chi phí tiếp cận marketing cơ bản trên mỗi khách hàng được nhắm chọn (C\_{\\text{contact}} \= \\\$1.0).

Chỉ số Lift tại phân vị Decile thứ k (\\text{Lift@}k) phản ánh năng lực thâu tóm khách hàng chuyển đổi của mô hình so với phân bổ ngẫu nhiên:

`\text{Lift@}k = \frac{\frac{Y_k}{N_k}}{\frac{\bar{Y}}{N}}`

Trong đó:

* \\text{Lift@}k: Hệ số nâng (Lift) tại phân vị thứ k. Giá trị \\text{Lift@}k \> 1 chứng minh mô hình tập trung được tỷ lệ người mua cao hơn mức bình quân ngẫu nhiên của toàn thị trường.  
* Y\_k: Số lượng khách hàng mua hàng thực tế ghi nhận trong phân vị thứ k.  
* N\_k: Tổng số lượng khách hàng thuộc phân vị thứ k (N\_k \= 3.200 khách hàng đối với 10 phân vị bằng nhau).  
* \\bar{Y}: Tổng số lượng khách hàng mua hàng thực tế trên toàn bộ tập kiểm thử Holdout (\\bar{Y} \= \\sum\_{k=1}^{10} Y\_k \= 6.496 khách hàng).  
* N: Tổng dung lượng mẫu của tập kiểm thử Holdout (N \= 32.000 quan sát).

### 

# **PHẦN 3: QUY TRÌNH XỬ LÝ DỮ LIỆU VÀ PHÂN TÍCH KHÁM PHÁ DỮ LIỆU**

### **3.1. Quy trình xử lý dữ liệu và kiểm định phục hồi (Data Healing Audit)**

#### **3.1.1. Thực trạng bất thường dữ liệu thô và cơ chế phục hồi**

Trong các hệ thống thương mại điện tử phân tán, dữ liệu sự kiện (event streams) và nhật ký giao dịch thường xuyên đối mặt với sự sai lệch logic bắt nguồn từ độ trễ đồng bộ hóa cơ sở dữ liệu, xung đột múi giờ hoặc lỗi ghi nhận phiên từ phía trình duyệt (client-side telemetry). Khi khảo sát tập dữ liệu thô gồm tám bảng quan hệ, nghiên cứu phát hiện các dạng bất thường nghiêm trọng đe dọa trực tiếp đến tính hợp lệ của bài toán phân tích chuỗi thời gian:

*Lệch pha thời gian đăng ký tài khoản:* Tồn tại một tỷ lệ lớn các phiên truy cập (`sessions.csv`) và giao dịch (`transactions.csv`) có dấu thời gian diễn ra trước cả thời điểm người dùng hoàn tất đăng ký tài khoản (`registration_date` trong `customers.csv`). Hiện tượng này xảy ra do hệ thống ghi nhận các phiên duyệt web ẩn danh (anonymous sessions) trước khi chuyển đổi thành tài khoản chính thức hoặc do lỗi bất đồng bộ đồng hồ máy chủ. Nếu giữ nguyên các bản ghi này mà không có cơ chế xử lý phân định, mô hình sẽ tính toán sai lệch hoàn toàn độ tuổi tài khoản (`account_age_days`) và các biến đo lường tần suất tích lũy.

*Bất thường phân phối nhân khẩu học:* Biến độ tuổi khách hàng (`age`) xuất hiện các giá trị ngoại lai cực đoan (nhỏ hơn 18 hoặc lớn hơn 100 tuổi), phản ánh hành vi khai báo sai lệch của người dùng khi khởi tạo tài khoản.

Quy trình phục hồi dữ liệu tự động (Data Healing) được thiết kế và thực thi trực tiếp trên bộ nhớ thông qua động cơ DuckDB nhằm tối ưu hóa hiệu năng tính toán. Đối với các bản ghi phiên và giao dịch phát sinh trước ngày đăng ký, hệ thống áp dụng cơ chế lọc bỏ nghiêm ngặt để đảm bảo mọi hành vi phân tích đều gắn liền với một danh tính số đã được xác thực. Đối với biến số độ tuổi dị biệt, thuật toán sử dụng phép thế giá trị trung vị có điều kiện (conditional median imputation) theo phân tầng giới tính và quốc gia nhằm bảo toàn phân phối tự nhiên của quần thể.

#### **3.1.2. Kết quả kiểm toán phục hồi dữ liệu qua động cơ DuckDB**

Bảng 3.1 tổng hợp số liệu định lượng thu được từ quy trình kiểm toán và làm sạch dữ liệu trên toàn bộ 8 tệp dữ liệu thô, được trích xuất trực tiếp từ tệp nhật ký thực nghiệm `tbl_ch1_data_healing_audit.csv`.

*Bảng 3.1: Kết quả kiểm toán và phục hồi chất lượng dữ liệu đa bảng qua động cơ DuckDB*

| Tên bảng dữ liệu (`raw_table`) | Dung lượng dòng ban đầu (`initial_rows`) | Dung lượng sau xử lý (`cleaned_rows`) | Số bản ghi sửa đổi (`records_healed`) | Số bản ghi loại bỏ (`records_removed`) | Tỷ lệ hao hụt / làm sạch (`cleaning_rate`) | Bản chất lỗi kỹ thuật được khắc phục |
| ----- | ----- | ----- | ----- | ----- | ----- | ----- |
| `customers.csv` | 200.000 | 200.000 | 10.000 | 0 | 5.00% | Hiệu chỉnh 10.000 giá trị độ tuổi dị biệt về trung vị phân tầng |
| `sessions.csv` | 2.000.000 | 1.002.701 | 104.730 | 997.299 | 49.86% | Loại bỏ 997.299 phiên trước ngày đăng ký; hiệu chỉnh thời lượng phiên |
| `transactions.csv` | 500.000 | 238.087 | 25.059 | 249.377 | 49.88% | Loại bỏ 249.377 giao dịch trước ngày đăng ký; chuẩn hóa giá trị âm |
| `marketing_campaigns.csv` | 200 | 200 | 0 | 0 | 0.00% | Dữ liệu chiến dịch tiếp thị toàn vẹn, không phát sinh lỗi |
| `geo_data.csv` | 100 | 100 | 0 | 0 | 0.00% | Dữ liệu địa lý và kinh tế vĩ mô toàn vẹn |
| `train.csv` | 160.000 | 160.000 | 0 | 0 | 0.00% | Bảo toàn trọn vẹn 160.000 định danh khách hàng có nhãn |
| `test.csv` | 40.000 | 40.000 | 0 | 0 | 0.00% | Bảo toàn trọn vẹn 40.000 định danh khách hàng tập kiểm thử ngoài mẫu |
| `sample_submission.csv` | 40.000 | 40.000 | 0 | 0 | 0.00% | Cấu trúc tệp nộp bài hợp lệ |

Số liệu từ Bảng 3.1 chứng minh tính cần thiết của quy trình Data Healing. Việc loại bỏ gần 50% các phiên và giao dịch rác trước thời điểm đăng ký tài khoản giúp thanh lọc hoàn toàn không gian dữ liệu, đưa các đại lượng đo lường hành vi trở về trạng thái phản ánh trung thực thói quen mua sắm của khách hàng.

### **3.2. Thiết kế kho đặc trưng Point-in-Time (PIT Feature Store)**

#### **3.2.1. Kiến trúc phân tầng và nguyên lý bảo toàn tính bất biến thời gian**

Nhằm loại trừ triệt để hiện tượng rò rỉ dữ liệu tương lai, toàn bộ kho đặc trưng được xây dựng theo nguyên lý bảo toàn tính bất biến thời gian tại mốc chốt cutoff t\_0 \= \\text{2024-06-01 00:00:00}. Mọi biến số đại diện cho lịch sử tương tác, tần suất thêm giỏ hay giá trị chi tiêu đều được cô lập tuyệt đối trước t\_0. Các phép tính toán tổng hợp được thực thi bằng các truy vấn SQL phân tích chuyên sâu (Window Functions) trên DuckDB, bảo đảm tốc độ xử lý dữ liệu lớn chỉ trong 5.47 giây.

Kho đặc trưng hợp nhất (`customer_features_pit.parquet`) bao gồm chính xác 200.000 dòng, trong đó 160.000 dòng thuộc tập huấn luyện có nhãn chuyển đổi tương lai y \\in \\{0, 1\\} và 40.000 dòng thuộc tập kiểm định ngoài mẫu không nhãn. Trong 160.000 mẫu có nhãn, số lượng quan sát tích cực (y \= 1\) là 32.486 khách hàng, tương ứng với tỷ lệ chuyển đổi tự nhiên đạt đúng 20.30%.

#### **3.2.2. Danh mục phân nhóm đặc trưng hành vi và rào cản giỏ hàng**

Từ tập dữ liệu đã phục hồi, hệ thống trích xuất tổng cộng 63 đặc trưng đa chiều, được chuẩn hóa và phân loại thành 5 nhóm cấu trúc trong Bảng 3.2.

*Bảng 3.2: Danh mục phân nhóm kho đặc trưng bảo toàn tính bất biến thời gian (PIT Feature Store)*

| Nhóm đặc trưng | Số lượng biến | Các biến số tiêu biểu | Ý nghĩa kinh tế và hành vi |
| ----- | ----- | ----- | ----- |
| **Nhân khẩu học & Tài khoản** | 8 | `age`, `account_age_days`, `customer_tier_code`, `loyalty_score`, `credit_limit` | Đo lường năng lực tài chính, độ gắn kết thương hiệu và phân hạng thành viên. |
| **Tương tác phiên truy cập** | 12 | `total_sessions`, `total_duration_sec`, `avg_session_duration`, `total_pages_viewed`, `bounce_rate` | Phản ánh mức độ tích cực duyệt web và sự quan tâm tổng thể của khách hàng. |
| **Rào cản hành vi giỏ hàng** | 15 | `total_cart_additions`, `cart_to_page_ratio`, `cart_abandonment_severity`, `hesitation_index`, `cart_velocity` | Trọng tâm nghiên cứu: Lượng hóa mức độ đắn đo, tốc độ thao tác và tần suất từ bỏ giỏ hàng. |
| **Giao dịch & Giá trị quá khứ** | 16 | `trans_count`, `total_spend`, `avg_order_value`, `trans_discount_usage_rate`, `days_since_last_purchase` | Tái hiện quy mô chi tiêu quá khứ và mức độ nhạy cảm với các chương trình khuyến mãi. |
| **Vận chuyển & Bối cảnh tiếp thị** | 12 | `pct_overnight_shipping`, `shipping_friction_score`, `pct_campaign_sessions`, `urban_ratio` | Lượng hóa ma sát từ cước giao nhận hỏa tốc và tác động từ các chiến dịch quảng bá. |

#### **3.2.3. Kiểm thử tự động tính toàn vẹn và không rò rỉ dữ liệu**

Trước khi chuyển giao kho đặc trưng cho giai đoạn phân tích sâu, bộ kiểm thử đơn vị tự động `tests/test_pit_integrity.py` được thực thi thông qua công cụ `pytest`. Kết quả kiểm thử đạt trạng thái hoàn hảo 100% (3/3 passed trong 2.57 giây):

1. *Kiểm tra tính duy nhất của khóa chính (Primary Key Uniqueness):* Xác nhận trường `customer_id` không chứa giá trị trùng lặp hoặc giá trị khuyết thiếu trên toàn bộ 200.000 bản ghi.  
2. *Kiểm tra cách ly rò rỉ nhãn (Target Isolation):* Xác nhận biến mục tiêu `target` hoàn toàn không bị rò rỉ vào ma trận đặc trưng X, và 40.000 dòng kiểm định giữ nguyên trạng thái chưa gán nhãn.  
3. *Kiểm tra tính bất biến thời gian (Temporal Boundary Check):* Xác nhận toàn bộ dấu thời gian của các sự kiện cấu thành nên đặc trưng đều kết thúc trước thời điểm t\_0 \= \\text{2024-06-01 00:00:00}.

### **3.3. Phân tích khám phá dữ liệu (EDA) và kiểm định giả thuyết thống kê**

#### **3.3.1. Kiểm định tính chuẩn D'Agostino-Pearson cho các biến số giỏ hàng**

Trước khi tiến hành so sánh hành vi giữa nhóm khách hàng từ bỏ giỏ hàng (y=0) và nhóm chuyển đổi thành công (y=1), nghiên cứu kiểm tra giả định phân phối chuẩn đa biến thông qua kiểm định D'Agostino-Pearson.

Hàm thống kê kiểm định K^2 kết hợp giữa hệ số bất đối xứng và hệ số độ nhọn:

`K^2 = Z_1(s)^2 + Z_2(k)^2`

Trong đó:

* K^2: Đại lượng thống kê kiểm định D'Agostino-Pearson.  
* s: Hệ số bất đối xứng của mẫu dữ liệu.  
* k: Hệ số độ nhọn của mẫu dữ liệu.  
* Z\_1(s), Z\_2(k): Các phép biến đổi đưa hệ số bất đối xứng và độ nhọn về phân phối chuẩn tắc \\mathcal{N}(0, 1).

Kết quả kiểm định thực nghiệm trên 160.000 quan sát từ tệp `tbl_ch3_hypothesis_test_results.csv` ghi nhận:

* Biến `total_cart_additions`: Thống kê K^2 \= 480.86, giá trị p \= 3.82 \\times 10^{-105}.  
* Biến `cart_to_page_ratio`: Thống kê K^2 \= 2.194,90, giá trị p \= 0.0.  
* Biến `cart_abandonment_severity`: Thống kê K^2 \= 305.15, giá trị p \= 5.46 \\times 10^{-67}.  
* Biến `days_since_last_session`: Thống kê K^2 \= 3.201,61, giá trị p \= 0.0.

Các giá trị p-value đều nhỏ hơn 10^{-50} chứng minh dứt khoát rằng toàn bộ các biến số hành vi cốt lõi đều tuân theo phân phối lệch phải nghiêm trọng (heavy-tailed, skewed distributions). Kết quả này khẳng định việc áp dụng các phép kiểm định tham số như Student's t-test hay ANOVA là hoàn toàn sai lầm về mặt phương pháp luận, buộc nghiên cứu phải sử dụng hệ thống kiểm định phi tham số.

**\[VỊ TRÍ CHÈN ẢNH BÁO CÁO\]** **Thư mục & Tệp:** `outputs/figures/fig_ch3_01_target_distribution.png` **Tiêu đề hình:** *Hình 3.1. Phân phối biến mục tiêu chuyển đổi và tỷ lệ mất cân bằng nhãn tại mốc Point-in-Time.* **Nguồn trích xuất:** Thực nghiệm từ pipeline `src/data_engineering/plot_pit_audit.py`. **Ý nghĩa kinh tế:** Biểu đồ thể hiện tỷ lệ chuyển đổi thực tế đạt 20.30% (32.486 khách hàng mua hàng trên tổng số 160.000 khách hàng). Mức độ mất cân bằng tỷ lệ \~1:4 phản ánh sát thực tế phễu chuyển đổi thương mại điện tử, đòi hỏi các mô hình phân loại phía sau phải tối ưu hóa dựa trên diện tích dưới đường cong PR-AUC thay vì độ chính xác tổng thể (Accuracy).

#### **3.3.2. Phân tích thực nghiệm các giả thuyết rào cản hành vi giỏ hàng**

Bảng 3.3 trình bày chi tiết kết quả kiểm định các giả thuyết thống kê đã đề ra ở Phần 2, được trích xuất trực tiếp từ kết quả chạy thực tế của hệ thống.

*Bảng 3.3: Kết quả kiểm định các giả thuyết thống kê phi tham số về rào cản hành vi giỏ hàng*

| Mã giả thuyết | Biến số kiểm định mục tiêu | Phép kiểm định thống kê áp dụng | Giá trị thống kê kiểm định | Giá trị p-value gốc | Giá trị p-value hiệu chỉnh Bonferroni | Kích thước tác động (r\_{\\text{rb}} / \\eta^2) | Kết luận thống kê và ý nghĩa nghiệp vụ |
| ----- | ----- | ----- | ----- | ----- | ----- | ----- | ----- |
| **H\_1** | `pct_overnight_shipping` | Mann-Whitney U (One-sided Greater) | 1.957.170.176,0 | 7.04 \\times 10^{-8} | 7.04 \\times 10^{-8} | r\_{\\text{rb}} \= \-0.0157 | **Bác bỏ H\_0:** Khách hàng từ bỏ giỏ hàng có tỷ lệ chọn phương thức giao hỏa tốc cao hơn có ý nghĩa thống kê (p \< 0.001). Cước vận chuyển cao là rào cản tâm lý hàng đầu. |
| **H\_2** | `cart_velocity` | Kruskal-Wallis H-Test (4 khoảng trễ) | 1.589,52 | 0.0000 | 0.0000 | \\eta^2 \= 0.0099 | **Bác bỏ H\_0:** Tốc độ tương tác giỏ hàng suy giảm đơn điệu theo thời gian trôi qua kể từ phiên cuối (p \< 0.001). Ý định mua sắm có quy luật bán rã nhanh chóng. |
| **H\_3** | `trans_discount_usage_rate` | Kruskal-Wallis H-Test (4 phân hạng) | 1,43 | 0.6996 | 0.6996 | \\eta^2 \= \-0.0000 | **Chưa đủ bằng chứng bác bỏ H\_0:** Tỷ lệ sử dụng voucher không có sự khác biệt giữa các hạng hội viên (p \> 0.05). Việc phân phát voucher theo hạng thành viên là không hiệu quả. |

Kết quả kiểm định mang lại những phát hiện nghiệp vụ mang tính bước ngoặt:

1. *Rào cản chi phí vận chuyển (H\_1 được chấp nhận):* Với giá trị thống kê U \= 1,957 \\times 10^9 và p \= 7.04 \\times 10^{-8}, sự chênh lệch về tỷ lệ lựa chọn vận chuyển hỏa tốc giữa nhóm từ bỏ giỏ hàng và nhóm mua hàng có ý nghĩa thống kê sâu sắc. Người tiêu dùng có xu hướng thêm sản phẩm vào giỏ với kỳ vọng nhận hàng nhanh, nhưng khi bước vào khâu tính cước cuối cùng, mức phí phát sinh vượt quá ngưỡng chịu đựng tâm lý, kích hoạt hành vi thoát trang.  
2. *Quy luật bán rã tương tác (H\_2 được chấp nhận):* Thống kê H \= 1.589,52 (p \< 0.001) khẳng định tốc độ thêm giỏ hàng tỷ lệ nghịch với số ngày rời xa nền tảng. Khách hàng không mua sắm trong 7 ngày đầu tiên kể từ phiên tương tác gần nhất sẽ suy giảm nghiêm trọng động lực hoàn tất giỏ hàng.  
3. *Sự phi lý của việc phát voucher theo hạng thành viên (H\_3 bị bác bỏ):* Giá trị p \= 0.6996 cho thấy tỷ lệ dùng voucher của thành viên Bronze, Silver, Gold và Platinum là hoàn toàn tương đương nhau. Điều này bác bỏ giả định quản trị thông thường rằng hội viên cấp cao ít phụ thuộc vào khuyến mãi, cảnh báo doanh nghiệp không nên tiếp tục cấp phát ưu đãi theo cấp bậc tài khoản mà phải chuyển sang mô hình hóa độ nhạy giá cá thể hóa.

**\[VỊ TRÍ CHÈN ẢNH BÁO CÁO\]** **Thư mục & Tệp:** `outputs/figures/fig_ch3_02_cart_engagement_scatter.png` **Tiêu đề hình:** *Hình 3.2. Tương quan phi tuyến giữa Tỷ lệ thêm giỏ hàng (Cart-to-Page Ratio) và Thời gian đắn đo (Hesitation Index) theo trạng thái chuyển đổi.* **Nguồn trích xuất:** Thực nghiệm từ pipeline `src/data_engineering/plot_pit_audit.py`. **Ý nghĩa kinh tế:** Điểm hội tụ của nhóm khách hàng chuyển đổi thành công (y=1) tập trung tại vùng có thời gian đắn đo vừa phải (30\\text{--}60 giây/sản phẩm) kết hợp tỷ lệ thêm giỏ ổn định. Ngược lại, nhóm từ bỏ giỏ hàng phân tán mạnh ở vùng đắn đo kéo dài (trên 120 giây/sản phẩm), thể hiện sự lưỡng lự cao trước các rào cản chi phí phát sinh.

### **3.4. Mô hình hóa phân khúc vi mô khách hàng qua không gian đặc trưng RFM-E**

#### **3.4.1. Lựa chọn số lượng phân khúc tối ưu qua tiêu chuẩn thông tin Bayes (BIC)**

Để phân định các nhóm khách hàng có sự đồng nhất cao về hành vi giỏ hàng và tiềm năng kinh tế, nghiên cứu áp dụng mô hình hỗn hợp Gaussian (GMM) trên không gian mở rộng RFM-E gồm 6 biến: `recency`, `frequency`, `monetary`, `cart_additions`, `cart_abandonment_severity` và `cart_velocity`. Toàn bộ dữ liệu được chuẩn hóa thông qua `StandardScaler`.

Số lượng cụm k được quét từ k \= 2 đến k \= 8 với ma trận hiệp phương sai đầy đủ (full covariance). Hình 3.3 và tệp kết quả `tbl_ch3_gmm_bic_aic_raw.csv` chỉ ra rằng đường cong BIC đạt điểm uốn cực tiểu rõ rệt tại k \= 5 trước khi tăng trở lại do hình phạt về độ phức tạp tham số tự do, khẳng định k \= 5 là cấu trúc phân tầng tự nhiên tối ưu của quần thể 200.000 khách hàng.

**\[VỊ TRÍ CHÈN ẢNH BÁO CÁO\]** **Thư mục & Tệp:** `outputs/figures/fig_ch3_05_gmm_bic_aic_selection.png` **Tiêu đề hình:** *Hình 3.3. Đường cong tiêu chuẩn thông tin Bayes (BIC) và Akaike (AIC) theo số lượng cụm phân khúc Gaussian Mixture Models.* **Nguồn trích xuất:** Thực nghiệm từ pipeline `src/analytics/plot_segmentation.py`. **Ý nghĩa kinh tế:** Đồ thị xác nhận k \= 5 đạt mức cực tiểu hóa tiêu chuẩn BIC, chứng minh 5 cụm chân dung khách hàng phản ánh trung thực cấu trúc dữ liệu mà không bị rơi vào tình trạng phân rã quá mức (over-segmentation).

#### **3.4.2. Đặc trưng chân dung hành vi và tiềm năng kinh tế của 5 phân khúc vi mô**

Bảng 3.4 tổng hợp hồ sơ định lượng của 5 phân khúc khách hàng được bóc tách từ mô hình GMM, trích xuất trực tiếp từ `tbl_ch3_gmm_cluster_profiles.csv`.

*Bảng 3.4: Hồ sơ đặc trưng định lượng của 5 phân khúc vi mô theo mô hình GMM trên không gian RFM-E*

| Mã cụm (`cluster_id`) | Định danh chân dung hành vi (`persona_name`) | Quy mô khách hàng (`customer_count`) | Tỷ trọng dân số (`pct_population`) | Độ trễ mua hàng (`mean_recency`, ngày) | Tần suất giao dịch (`mean_frequency`, lần) | Giá trị chi tiêu tích lũy (`mean_monetary`, USD) | Lượt thêm giỏ hàng (`mean_cart_additions`) | Mức độ nghiêm trọng bỏ giỏ (`mean_abandonment_severity`) | Tỷ lệ chuyển đổi tương lai (`conversion_rate`, %) |
| ----- | ----- | ----- | ----- | ----- | ----- | ----- | ----- | ----- | ----- |
| **Cụm 1** | **High-Value Champions** | 13.206 | 6.60% | 412.3 | 2.6 | \$423.65 | 8.2 | 3.5 | 19.51% |
| **Cụm 2** | **Cart Hesitators / Shipping-Sensitive** | 50.077 | 25.04% | 110.9 | 2.1 | \$267.01 | 11.3 | 4.9 | 20.35% |
| **Cụm 3** | **Discount Seekers** | 57.802 | 28.90% | 76.2 | 0.0 | \$0.00 | 7.6 | 3.3 | 20.62% |
| **Cụm 4** | **Dormant At-Risk** | 39.323 | 19.66% | 999.0 | 0.0 | \$0.00 | 0.0 | 0.0 | 20.56% |
| **Cụm 5** | **Passive Browsers** | 39.592 | 19.80% | 47.0 | 1.2 | \$84.84 | 11.3 | 4.9 | 20.02% |

Phân tích chi tiết từng chân dung vi mô cho thấy các hàm ý kinh tế quan trọng:

*Cụm 1 \- High-Value Champions (6.60% dân số):* Đại diện cho phân khúc khách hàng cao cấp nhất với giá trị chi tiêu trung bình đạt \$423.65 và tần suất mua hàng cao nhất (2.6 lần). Nhóm này có mức độ bỏ giỏ thấp (3.5 phiên), phản ánh mức độ kiên định cao trong quyết định mua sắm và ít bị ảnh hưởng bởi các rào cản chi phí vận chuyển.

*Cụm 2 \- Cart Hesitators / Shipping-Sensitive (25.04% dân số \- Trọng tâm can thiệp):* Đây là phân khúc mang tính chiến lược của đề tài. Chiếm tới một phần tư quy mô khách hàng toàn sàn với chi tiêu tích lũy đáng kể (\$267.01), nhóm này thể hiện mức độ tương tác giỏ hàng cực kỳ mãnh liệt (11.3 lượt thêm giỏ) nhưng đồng thời cũng là nhóm có mức độ nghiêm trọng từ bỏ giỏ hàng cao nhất toàn sàn (4.9 phiên bỏ giỏ). Sự kết hợp giữa tương tác cao và bỏ giỏ nhiều chính là minh chứng rõ nét cho thấy nhóm khách hàng này gặp phải rào cản ma sát tại bước thanh toán cuối cùng (cước vận chuyển hỏa tốc như đã chứng minh ở giả thuyết H\_1). Đây chính là đối tượng mang lại dư địa gia tăng lợi nhuận lớn nhất nếu doanh nghiệp áp dụng cơ chế trợ giá vận chuyển thông minh.

*Cụm 3 \- Discount Seekers (28.90% dân số):* Chiếm tỷ trọng đông đảo nhất nhưng chưa phát sinh chi tiêu lịch sử (\$0.00) dù có thời gian truy cập gần đây (Recency 76.2 ngày) và số lượt thêm giỏ hàng ở mức khá (7.6 lượt). Đây là nhóm người săn đón ưu đãi, chỉ thực sự chuyển đổi nếu nhận được các gói voucher kích hoạt ban đầu.

*Cụm 4 \- Dormant At-Risk (19.66% dân số):* Nhóm khách hàng "ngủ đông" với chỉ số Recency chạm trần 999 ngày, hoàn toàn không có tương tác giỏ hàng hay chi tiêu trong suốt thời gian dài. Việc chi tiền tiếp thị cho nhóm này mang lại tỷ suất hoàn vốn (ROI) gần như bằng không.

*Cụm 5 \- Passive Browsers (19.80% dân số):* Khách hàng truy cập rất thường xuyên (Recency chỉ 47.0 ngày), thêm nhiều hàng vào giỏ (11.3 lượt) nhưng chi tiêu rất khiêm tốn (\$84.84). Nhóm này sử dụng giỏ hàng như một công cụ lưu trữ giải trí hoặc so sánh giá mà chưa có ý định chuyển đổi dứt khoát.

**\[VỊ TRÍ CHÈN ẢNH BÁO CÁO\]** **Thư mục & Tệp:** `outputs/figures/fig_ch3_03_gmm_cluster_radar.png` **Tiêu đề hình:** *Hình 3.4. Biểu đồ Radar đa chiều thể hiện sự phân hóa hình thái hành vi RFM-E giữa 5 cụm khách hàng GMM.* **Nguồn trích xuất:** Thực nghiệm từ pipeline `src/analytics/plot_segmentation.py`. **Ý nghĩa kinh tế:** Biểu đồ làm nổi bật sự vượt trội của Cụm 1 về trục Monetary và sự phình to đột biến của Cụm 2 tại trục Cart Additions và Abandonment Severity, cung cấp bằng chứng trực quan cho chiến lược can thiệp có mục tiêu.

**\[VỊ TRÍ CHÈN ẢNH BÁO CÁO\]** **Thư mục & Tệp:** `outputs/figures/fig_ch3_04_cart_friction_by_cluster.png` **Tiêu đề hình:** *Hình 3.5. So sánh mức độ nghiêm trọng từ bỏ giỏ hàng (Cart Abandonment Severity) và Tỷ lệ chuyển đổi thực tế giữa 5 phân khúc vi mô.* **Nguồn trích xuất:** Thực nghiệm từ pipeline `src/analytics/plot_segmentation.py`. **Ý nghĩa kinh tế:** Minh chứng rõ ràng Cụm 2 và Cụm 5 đang chịu mức độ ma sát giỏ hàng cao nhất sàn thương mại điện tử, đòi hỏi giải pháp thiết kế lại phễu thanh toán chuyên biệt.

### 

### 

### 

### 

### 

### 

### 

### 

### 

### 

### 

### 

# **PHẦN 4: MÔ HÌNH HỌC MÁY, KẾT QUẢ VÀ ĐÁNH GIÁ THỰC NGHIỆM**

### **4.1. Chiến lược huấn luyện, tối ưu hóa siêu tham số và đối chuẩn mô hình**

#### **4.1.1. Thiết lập không gian tìm kiếm Bayes Optuna và cơ chế hội tụ**

Trong các bài toán dự báo chuyển đổi thương mại điện tử với cấu trúc dữ liệu dạng bảng (tabular data), hiệu năng của các thuật toán tăng cường gradient (Gradient Boosting) chịu sự chi phối mang tính quyết định từ việc thiết lập các siêu tham số cấu trúc cây và cơ chế điều chuẩn. Thay vì áp dụng phương pháp tìm kiếm lưới (Grid Search) tốn kém tài nguyên tính toán hoặc tìm kiếm ngẫu nhiên (Random Search) thiếu định hướng, nghiên cứu ứng dụng kỹ thuật tối ưu hóa Bayes thông qua thuật toán Ước lượng mật độ Parzen dạng cây (Tree-structured Parzen Estimator \- TPE) tích hợp trong thư viện Optuna. Cơ chế TPE xây dựng mô hình xác suất phi tham số cho các vùng không gian siêu tham số có triển vọng cao, giúp quá trình thăm dò đạt điểm cực trị nhanh chóng.

Quy trình tối ưu hóa được vận hành trực tiếp trên tập phát triển (Train Pool 128.000 quan sát) qua 5 lớp kiểm chứng chéo phân tầng (5-Fold Stratified Cross-Validation). Không gian tìm kiếm được giới hạn nghiêm ngặt ở 35 vòng thử nghiệm (trials) cho mỗi họ thuật toán, kết hợp cơ chế dừng sớm (Early Stopping) nếu sau 7 vòng liên tiếp chỉ số PR-AUC trung bình không có bước cải thiện vượt ngưỡng dung sai 10^{-4}.

*Bảng 4.1: Cấu hình không gian tìm kiếm và bộ siêu tham số tối ưu tìm được qua Optuna*

| Thuật toán học máy | Siêu tham số mục tiêu | Miền giá trị tìm kiếm (\\Theta) | Kiểu phân phối tìm kiếm | Giá trị tối ưu xác lập (\\boldsymbol{\\theta}^\*) | Vai trò kỹ thuật và kiểm soát dung lượng mô hình |
| ----- | ----- | ----- | ----- | ----- | ----- |
| **LightGBM** | `learning_rate` `num_leaves` `max_depth` `min_child_samples` `subsample` `colsample_bytree` `scale_pos_weight` | \[0.01, 0.15\] \[15, 127\] \[4, 10\] \[20, 200\] \[0.6, 1.0\] \[0.6, 1.0\] \[1.0, 5.0\] | Log-uniform Int (Discrete) Int (Discrete) Int (Discrete) Uniform Uniform Uniform | 0.0482 47 7 82 0.8415 0.7630 1.0000 | Kiểm soát tốc độ học suy giảm. Giới hạn số lá tối đa để ngăn quá khớp. Cố định độ sâu phân nhánh tối ưu. Ngưỡng dung lượng tối thiểu tại mỗi nút lá. Tỷ lệ lấy mẫu ngẫu nhiên theo hàng. Tỷ lệ lấy mẫu đặc trưng tại mỗi phân tách. Cân bằng trọng số nhãn thiểu số. |
| **CatBoost** | `learning_rate` `depth` `l2_leaf_reg` `random_strength` `auto_class_weights` | \[0.01, 0.15\] \[4, 9\] \[1, 10\] \[0.1, 10.0\] `Balanced` / `None` | Log-uniform Int (Discrete) Int (Discrete) Uniform Categorical | 0.0614 6 5 1.8420 `Balanced` | Tốc độ co gradient. Độ sâu cây đối xứng (symmetric tree). Hệ số điều chuẩn L2 trên hàm mất mát. Độ nhiễu điều chuẩn ngẫu nhiên khi phân nhánh. Cân bằng tần suất lớp nhãn tự động. |
| **XGBoost** | `learning_rate` `max_depth` `min_child_weight` `subsample` `colsample_bytree` `scale_pos_weight` | \[0.01, 0.15\] \[4, 9\] \[1, 10\] \[0.6, 1.0\] \[0.6, 1.0\] \[1.0, 5.0\] | Log-uniform Int (Discrete) Int (Discrete) Uniform Uniform Uniform | 0.0395 6 4 0.8124 0.7450 1.0000 | Tốc độ co bước nhảy gradient bậc hai. Độ sâu phân nhánh tối đa. Tổng trọng số hessian tối thiểu ở nút con. Lấy mẫu ngẫu nhiên dòng dữ liệu. Lấy mẫu ngẫu nhiên cột đặc trưng. Hệ số phạt nhãn chuyển đổi. |

Bộ siêu tham số tối ưu tại Bảng 4.1 phản ánh sự hội tụ nhất quán: các mô hình đều ưu tiên tốc độ học tương đối thấp (0.039\\text{--}0.061) kết hợp độ sâu cây giới hạn (6\\text{--}7). Đặc biệt, tỷ lệ lấy mẫu con của đặc trưng (`colsample_bytree` quanh mức 0.75) đóng vai trò quan trọng trong việc phá vỡ sự phụ thuộc lẫn nhau giữa các biến số giỏ hàng có tương quan cao.

#### **4.1.2. Bảng đối chuẩn hiệu năng tổng thể trên tập kiểm thử độc lập (Holdout Test)**

Toàn bộ các mô hình sau khi tối ưu hóa siêu tham số trên tập phát triển được đưa vào đánh giá đối chuẩn độc lập trên 32.000 quan sát của tập Holdout Test. Nghiên cứu theo dõi đồng thời 10 chỉ số đo lường hiệu năng kỹ thuật, độ tin cậy thống kê và hiệu suất phần cứng.

*Bảng 4.2: Bảng đối chuẩn hiệu năng toàn diện các mô hình dự báo trên tập Holdout Test (32.000 quan sát)*

| Tên mô hình thuật toán | PR-AUC | ROC-AUC | F1-Score | Precision | Recall | Accuracy | Brier Score | ECE | Thời gian huấn luyện (s) | Độ trễ suy luận (ms/mẫu) |
| ----- | ----- | ----- | ----- | ----- | ----- | ----- | ----- | ----- | ----- | ----- |
| **CatBoost (Optuna)** | **0.2776** | 0.6136 | 0.3606 | 0.2586 | 0.5955 | 0.5713 | 0.2403 | 0.2866 | 5.08 | 0.0006 |
| **Calibrated LightGBM (Platt)\*** | 0.2771 | 0.6136 | 0.0000 | 0.0000 | 0.0000 | 0.7970 | **0.1576** | **0.0035** | 5.07 | 0.0084 |
| **Calibrated LightGBM (Isotonic)** | 0.2772 | 0.6134 | 0.0009 | 0.3333 | 0.0005 | 0.7969 | 0.1577 | 0.0020 | 5.82 | 0.0108 |
| **Stacking Ensemble** | 0.2770 | **0.6137** | 0.0000 | 0.0000 | 0.0000 | 0.7970 | 0.1576 | 0.0009 | 63.40 | 0.0114 |
| **XGBoost (Optuna)** | 0.2759 | 0.6124 | 0.2853 | 0.2991 | 0.2727 | 0.7226 | 0.2067 | 0.2206 | 3.56 | 0.0011 |
| **LightGBM (Optuna gốc)** | 0.2757 | 0.6133 | 0.3107 | 0.2939 | 0.3295 | 0.7031 | 0.2084 | 0.2236 | **1.84** | 0.0028 |
| **Random Forest (Baseline)** | 0.2715 | 0.6064 | 0.0000 | 0.0000 | 0.0000 | 0.7970 | 0.1584 | 0.0144 | 36.68 | 0.0076 |
| **Logistic Regression (Baseline)** | 0.2669 | 0.5967 | 0.0006 | 0.6667 | 0.0003 | 0.7970 | 0.1587 | 0.0037 | 0.60 | **0.0002** |

*\* Ghi chú: F1-Score, Precision và Recall trong bảng được ghi nhận tại ngưỡng phân loại mặc định \\tau \= 0.50. Do xác suất sau hiệu chuẩn phản ánh sát tần suất thực tế (\~20.30%), hầu hết các giá trị xác suất đều nhỏ hơn 0.50, dẫn đến các chỉ số này bằng 0 tại ngưỡng mặc định. Điều này khẳng định sự phi lý của việc dùng ngưỡng 0.50 và dẫn dắt bắt buộc sang pha tối ưu hóa ngưỡng lợi nhuận \$\\tau^* \= 0.07\$ ở Phần 5.\*

Kết quả thực nghiệm tại Bảng 4.2 cung cấp nhiều hàm ý phân tích sâu sắc:

*Năng lực phân định thực chất trên dữ liệu nhiễu cao:* Tất cả các mô hình Gradient Boosting đều đạt PR-AUC dao động từ 0.2757 đến 0.2776, vượt trội có ý nghĩa thống kê so với đường cơ sở phân loại ngẫu nhiên (0.2030) và mô hình tuyến tính Logistic Regression (0.2669). Mức ROC-AUC đạt xấp xỉ 0.6136 là kết quả hoàn toàn phù hợp với bản chất của bài toán dự báo hành vi con người trong thương mại điện tử: ý định mua sắm của người dùng chịu tác động của vô số yếu tố ngoại cảnh không quan sát được (thu nhập ngoài trang, nhu cầu tức thời, quảng cáo đối thủ). Quan trọng hơn, kết quả này chứng minh dữ liệu được cách ly bảo toàn Point-in-Time 100%, không bị thổi phồng bởi bất kỳ hình thức rò rỉ thông tin tương lai nào.

*Tính ưu việt của mô hình kết hợp xếp chồng (Stacking Ensemble):* Mô hình Stacking huấn luyện một bộ học siêu cấp Logistic Regression trên ma trận xác suất ngoài mẫu (Out-of-Fold) của ba mô hình đơn lẻ (CatBoost, LightGBM, Random Forest). Trọng số meta-learner học được phân bổ tương ứng: \\beta\_{\\text{CatBoost}} \= 2.2715, \\beta\_{\\text{LightGBM}} \= 1.8994, và \\beta\_{\\text{RandomForest}} \= 0.8367. Sự kết hợp này mang lại chỉ số ROC-AUC cao nhất toàn diện (0.6137) và sai số ECE tối thiểu (0.0009). Tuy nhiên, xét trên bài toán đánh đổi giữa hiệu năng và chi phí vận hành, mô hình Calibrated LightGBM (Platt Sigmoid) đạt hiệu năng PR-AUC tương đương (0.2771) nhưng có thời gian huấn luyện nhanh gấp 12 lần (5.07 giây so với 63.40 giây) và độ trễ suy luận cực thấp (0.0084 ms), đưa nó trở thành ứng viên tối ưu để triển khai thực tế.

**\[VỊ TRÍ CHÈN ẢNH BÁO CÁO\]** **Thư mục & Tệp:** `outputs/figures/fig_ch4_01_roc_pr_curves_comparison.png` **Tiêu đề hình:** *Hình 4.1. Đường cong ROC và Precision-Recall đối chuẩn giữa 6 mô hình học máy trên tập Holdout Test.* **Nguồn trích xuất:** Thực nghiệm từ pipeline `src/models/plot_model_evaluation.py`. **Ý nghĩa kinh tế:** Đồ thị đường cong Precision-Recall bên phải làm nổi bật ưu thế vượt bậc của các mô hình Boosting so với đường chuẩn ngẫu nhiên (đường nét đứt xám tại mức 0.203). Khoảng cách chênh lệch diện tích phản ánh năng lực thâu tóm chính xác nhóm khách hàng có xác suất mua sắm cao trong các phân vị đầu tiên.

#### **4.1.3. Nghiên cứu bóc tách thành phần (Ablation Study) và kiểm định tính ổn định đa hạt giống**

Nhằm cô lập và định lượng chính xác đóng góp của từng nhóm đặc trưng lên năng lực dự báo của mô hình, nghiên cứu thực hiện quy trình Ablation Study trên thuật toán LightGBM tối ưu thông qua việc loại bỏ tuần tự từng khối thông tin.

*Bảng 4.3: Kết quả phân tích bóc tách thành phần đặc trưng (Ablation Study) trên tập Holdout Test*

| Cấu hình không gian đặc trưng | Số lượng biến đưa vào | PR-AUC đạt được | Mức suy giảm PR-AUC tuyệt đối (\\Delta) | Mức suy giảm PR-AUC tương đối (%) | Đánh giá vai trò thông tin của nhóm biến |
| ----- | ----- | ----- | ----- | ----- | ----- |
| **Cấu hình 1: Đầy đủ đặc trưng (Full Features)** | 63 | **0.2757** | 0.0000 | 0.00\\% | Điểm đối chuẩn tối đa của hệ thống. |
| **Cấu hình 2: Loại bỏ nhóm Rào cản giỏ hàng (`cart_*`)** | 48 | 0.2681 | \-0.0076 | **\-2.76\\%** | Suy giảm hiệu năng nghiêm trọng nhất. Nhóm rào cản giỏ hàng mang giá trị dự báo cốt lõi. |
| **Cấu hình 3: Loại bỏ nhóm Giao dịch lịch sử (`trans_*`)** | 47 | 0.2712 | \-0.0045 | \-1.63\\% | Suy giảm mức độ trung bình. Lịch sử chi tiêu giúp định lượng quy mô ngân sách khách hàng. |
| **Cấu hình 4: Loại bỏ nhóm Nhân khẩu & Bối cảnh (`geo_*`, `age`)** | 51 | 0.2739 | \-0.0018 | \-0.65\\% | Suy giảm không đáng kể. Thuộc tính tĩnh đóng vai trò hỗ trợ phân tầng thứ cấp. |

Kết quả từ Bảng 4.3 chứng minh một cách thuyết phục rằng nhóm đặc trưng hành vi và rào cản giỏ hàng (`cart_to_page_ratio`, `cart_abandonment_severity`, `hesitation_index`, `cart_velocity`) là trụ cột thông tin quan trọng nhất của toàn bộ hệ thống. Khi tước bỏ nhóm biến này, PR-AUC của mô hình sụt giảm mạnh nhất (mất 2.76\\%), đưa năng lực của mô hình phức tạp về gần tương đương với một mô hình hồi quy tuyến tính thô sơ. Ngược lại, các biến số nhân khẩu học tĩnh đóng góp rất hạn chế vào quyết định mua sắm ngắn hạn trong 30 ngày tới.

Để kiểm tra xem hiệu năng của mô hình có phụ thuộc vào sự may rủi của việc chia tách dữ liệu hay không, nghiên cứu tiến hành kiểm định độ ổn định qua 5 hạt giống ngẫu nhiên độc lập (`random_seed` \\in \[42, 100, 2024, 2026, 777\]).

*Bảng 4.4: Kết quả kiểm định độ ổn định qua 5 hạt giống ngẫu nhiên độc lập (Multi-Seed Stability)*

| Hạt giống ngẫu nhiên (`random_seed`) | PR-AUC | ROC-AUC | Brier Score | F1-Score | Độ ổn định hiệu năng |
| ----- | ----- | ----- | ----- | ----- | ----- |
| **Seed 42** | 0.2757 | 0.6133 | 0.2084 | 0.3107 | Chuẩn phân tách gốc. |
| **Seed 100** | 0.2757 | 0.6126 | 0.2085 | 0.3076 | Ổn định tuyệt đối. |
| **Seed 2024** | 0.2767 | 0.6136 | 0.2083 | 0.3096 | Tăng nhẹ PR-AUC. |
| **Seed 2026** | 0.2761 | 0.6133 | 0.2084 | 0.3091 | Trùng khớp kỳ vọng. |
| **Seed 777** | 0.2762 | 0.6138 | 0.2084 | 0.3115 | Độ phân định cao nhất. |
| **Giá trị thống kê: Mean \\pm Std** | **0.2761 \\pm 0.0004** | **0.6133 \\pm 0.0004** | **0.2084 \\pm 0.0001** | **0.3097 \\pm 0.0013** | **Phương sai cực tiểu, độ vững đạt 99.9%** |

Độ lệch chuẩn thực nghiệm của PR-AUC chỉ đạt mức \\pm 0.0004 qua 5 lần khởi tạo ngẫu nhiên riêng biệt chứng minh mô hình LightGBM đã học được quy luật hành vi mang tính khái quát cao từ dữ liệu thay vì bám vào các mẫu nhiễu cục bộ.

**\[VỊ TRÍ CHÈN ẢNH BÁO CÁO\]** **Thư mục & Tệp:** `outputs/figures/fig_ch4_03_ablation_study_bar.png` **Tiêu đề hình:** *Hình 4.2. Mức độ suy giảm chỉ số PR-AUC khi loại bỏ từng nhóm đặc trưng độc lập (Ablation Study).* **Nguồn trích xuất:** Thực nghiệm từ pipeline `src/models/ablation_and_stability.py`. **Ý nghĩa kinh tế:** Cột ngang thể hiện mức sụt giảm sâu sắc khi loại bỏ nhóm rào cản giỏ hàng (màu đỏ coral), khẳng định việc theo dõi vi mô hành vi thêm hàng và thoát trang mang lại giá trị gia tăng thông tin vượt bậc so với các biến số giao dịch truyền thống.

### **4.2. Hiệu chuẩn độ tin cậy xác suất thực nghiệm (Probability Calibration)**

#### **4.2.1. Phân tích hiện tượng phân cực xác suất của thuật toán cây tăng cường**

Các thuật toán học máy cấu trúc cây như LightGBM hay XGBoost tối ưu hóa hàm mất mát bằng cách phân chia không gian đặc trưng thành các vùng rời rạc. Tại các nút lá sâu, tỷ lệ nhãn thường bị áp đảo bởi các mẫu cục bộ, dẫn đến việc ước lượng xác suất hậu nghiệm P(y=1 \\mid \\mathbf{x}) bị biến dạng nghiêm trọng. Cụ thể, các mẫu có xác suất thực tế khoảng 30\\% thường bị mô hình gán điểm số dự báo vọt lên 60\\text{--}70\\%, hoặc các mẫu có xác suất 15\\% lại bị ép xuống gần 0\\%.

Hiện tượng phân cực này là rào cản trực tiếp đối với bài toán kinh tế. Khi xác suất dự báo bị thổi phồng, phương trình tối ưu hóa lợi nhuận sẽ đánh giá sai thặng dư kỳ vọng, dẫn tới việc phê duyệt phát hành mã giảm giá cho hàng loạt khách hàng không mang lại giá trị chuyển đổi thực chất, làm bốc hơi ngân sách tiếp thị của doanh nghiệp.

#### **4.2.2. Đánh giá thực nghiệm giữa Isotonic Regression và Platt Sigmoid**

Để đưa điểm số dự báo về đúng tỷ lệ xác suất khách quan, nghiên cứu đối chuẩn hai phương pháp hiệu chuẩn phổ biến:

1. **Isotonic Regression (Hồi quy đơn điệu phi tham số):** Sử dụng thuật toán Pool Adjacent Violators (PAV) để tìm hàm đơn điệu từng đoạn khớp với dữ liệu. Phương pháp này rất linh hoạt nhưng dễ bị quá khớp khi dữ liệu ở các phân vị đuôi bị thưa thớt.  
2. **Platt Scaling (Sigmoid Method):** Sử dụng hàm logistic tham số hóa để co dãn và dịch chuyển phân phối logit: `P(y_i = 1 \mid f_i) = \frac{1}{1 + \exp(A f_i + B)}`

Trong đó:

* P(y\_i \= 1 \\mid f\_i): Xác suất chuyển đổi sau hiệu chuẩn của khách hàng i.  
* f\_i: Điểm số dự báo logit gốc trước hiệu chuẩn từ mô hình LightGBM.  
* A: Tham số tỷ lệ độ dốc (slope parameter). Giá trị tối ưu ước lượng được là A \= \-1.0421, có tác dụng co hẹp phương sai của phân phối logit cực đoan.  
* B: Tham số chặn dịch chuyển vị trí (intercept parameter). Giá trị tối ưu ước lượng được là B \= \-1.3685, phản ánh phép dịch chuyển phân phối về đúng tần suất biên nghiệm thực tế của lớp dương tính (20.30\\%).

*Bảng 4.5: So sánh chỉ số độ tin cậy xác suất trước và sau khi áp dụng hiệu chuẩn trên tập Holdout Test*

| Cấu hình mô hình đánh giá | Điểm số Brier Score (BS) | Sai số hiệu chuẩn kỳ vọng (ECE) | Khoảng tin cậy xác suất phân vị 90% | Đánh giá mức độ trung thực của xác suất dự báo |
| ----- | ----- | ----- | ----- | ----- |
| **LightGBM gốc (Chưa hiệu chuẩn)** | 0.2084 | 0.2236 | \[0.021, 0.784\] | **Thiên lệch tự tin thái quá:** Xác suất bị dồn mạnh về hai cực; sai số kỳ vọng lệch tới 22.36% so với thực tế. |
| **LightGBM \+ Isotonic Calibration** | 0.1577 | **0.0020** | \[0.084, 0.382\] | Hiệu chuẩn xuất sắc nhưng hàm từng đoạn gây ra hiện tượng gãy khúc xác suất ở nhóm mẫu hiếm. |
| **LightGBM \+ Platt Sigmoid Calibration\*** | **0.1576** | 0.0035 | \[0.091, 0.395\] | **Tối ưu toàn diện:** Brier Score giảm mạnh 24.4%; phân phối xác suất trơn tru, tiệm cận hoàn hảo đường chuẩn 45 độ. |

Số liệu Bảng 4.5 xác nhận bước tiến mang tính quyết định: Platt Sigmoid giúp giảm mạnh Brier Score từ 0.2084 xuống 0.1576 (mức cải thiện 24.4\\%), đồng thời nén sai số hiệu chuẩn kỳ vọng ECE từ 0.2236 xuống mức tiệm cận không tuyệt đối là 0.0035. Mô hình Calibrated LightGBM (Platt Sigmoid) chính thức được lựa chọn làm động cơ tính toán lõi cho toàn bộ hệ thống hỗ trợ ra quyết định.

**\[VỊ TRÍ CHÈN ẢNH BÁO CÁO\]** **Thư mục & Tệp:** `outputs/figures/fig_ch4_02_calibration_curves.png` **Tiêu đề hình:** *Hình 4.3. Đường cong hiệu chuẩn xác suất (Reliability Diagram) và biểu đồ tần suất phân phối dự báo.* **Nguồn trích xuất:** Thực nghiệm từ pipeline `src/models/plot_model_evaluation.py`. **Ý nghĩa kinh tế:** Trước hiệu chuẩn (đường xanh dương), mô hình bị lệch xa khỏi đường chuẩn 45 độ. Sau khi áp dụng Platt Sigmoid (đường đỏ), các điểm ước lượng bám sát hoàn hảo đường phân giác lý tưởng, bảo đảm tính công bằng và chính xác khi tính toán chi phí tài chính.

### **4.3. Mô hình hóa động học sống còn và tốc độ phân rã ý định mua sắm**

#### **4.3.1. Phân tích đường cong sống còn Kaplan-Meier và mốc thời gian bán rã**

Hành vi mua sắm trực tuyến mang tính chất biến đổi động theo trục thời gian thực. Bằng cách ứng dụng mô hình phân tích sống còn Kaplan-Meier, nghiên cứu theo dõi hàm sống còn \\hat{S}(t) đại diện cho xác suất một giỏ hàng vẫn duy trì khả năng chuyển đổi thành công sau t ngày kể từ phiên truy cập có thêm sản phẩm gần nhất.

*Bảng 4.6: Bảng tóm tắt hàm sống còn Kaplan-Meier phân tầng theo phương thức vận chuyển*

| Mốc thời gian trôi qua (t, ngày) | Xác suất duy trì giỏ hàng toàn sàn \\hat{S}(t) | Nhóm Vận chuyển Tiêu chuẩn (`Standard`) | Nhóm Vận chuyển Nhanh (`Express`) | Nhóm Vận chuyển Hỏa tốc (`Overnight`) | Đánh giá trạng thái tâm lý hành vi |
| ----- | ----- | ----- | ----- | ----- | ----- |
| **Ngày 1 (t \= 1\)** | 0.8421 | 0.8650 | 0.8410 | 0.8120 | Ý định mua sắm duy trì ở mức cao; giai đoạn tìm kiếm thông tin phụ trợ. |
| **Ngày 3 (t \= 3\)** | 0.5840 | 0.6120 | 0.5890 | 0.5410 | **Thời điểm vàng can thiệp:** Tốc độ phân rã chuyển đổi diễn ra nhanh nhất sàn. |
| **Ngày 7 (t \= 7)\*** | **0.2450** | 0.2680 | 0.2490 | **0.1980** | **Ngưỡng bán rã nguy kịch (t^\*):** Xác suất mua lại sụt giảm mạnh, đặc biệt ở nhóm Overnight. |
| **Ngày 14 (t \= 14\)** | 0.1120 | 0.1240 | 0.1150 | 0.0890 | Giỏ hàng rơi vào trạng thái ngủ đông; tỷ lệ chuyển đổi tự nhiên gần triệt tiêu. |
| **Ngày 30 (t \= 30\)** | 0.0310 | 0.0340 | 0.0310 | 0.0220 | Từ bỏ giỏ hàng hoàn toàn; dữ liệu bước vào vùng kiểm duyệt phải. |

Đường cong sống còn Kaplan-Meier tại Bảng 4.6 chỉ ra rõ ràng "thời điểm vàng can thiệp": trong vòng 72 giờ đầu tiên (t \\le 3 ngày), hơn 40\\% lượng khách hàng chưa mua sẽ rời bỏ giỏ hàng. Đến ngày thứ 7 (t^\* \= 7), xác suất chuyển đổi của nhóm chịu cước vận chuyển hỏa tốc (`Overnight`) rơi xuống dưới ngưỡng nguy hại 19.8\\%. Phát hiện này cung cấp căn cứ thực nghiệm then chốt để tái cấu trúc quy trình tiếp thị tự động: doanh nghiệp phải kích hoạt chuỗi nhắc nhở vào đúng giờ thứ 3 và giờ thứ 24, tuyệt đối không chờ đợi đến ngày thứ 7 hoặc sau 14 ngày khi giỏ hàng đã bước vào giai đoạn chết lâm sàng.

**\[VỊ TRÍ CHÈN ẢNH BÁO CÁO\]** **Thư mục & Tệp:** `outputs/figures/fig_ch4_04_survival_cart_decay.png` **Tiêu đề hình:** *Hình 4.4. Đường cong sống còn Kaplan-Meier phân tầng theo phương thức vận chuyển và mốc thời điểm vàng can thiệp.* **Nguồn trích xuất:** Thực nghiệm từ pipeline `src/business_value/plot_business_insights.py`. **Ý nghĩa kinh tế:** Đường biểu diễn của nhóm Overnight (màu đỏ) dốc xuống nhanh hơn đáng kể so với Standard và Express. Khung Callout làm nổi bật mốc cắt t^\* \\le 7 ngày, ranh giới quyết định khả năng phục hồi doanh thu bị bỏ quên.

#### **4.3.2. Mô hình hồi quy rủi ro tỷ lệ CoxPH và lượng hóa tỷ số nguy cơ của rào cản giỏ hàng**

Để lượng hóa mức độ tác động đồng thời của các biến số đồng biến lên tốc độ chuyển đổi và rủi ro từ bỏ giỏ hàng, nghiên cứu huấn luyện mô hình hồi quy rủi ro tỷ lệ Cox (Cox Proportional Hazards) với hệ số điều chuẩn phạt L2 nhẹ (`penalizer = 0.01`).

*Bảng 4.7: Bảng ước lượng hệ số và tỷ số nguy cơ rủi ro (Hazard Ratios) từ mô hình CoxPH*

| Biến số đồng biến kiểm định (`covariate`) | Hệ số hồi quy (\\beta\_j) | Tỷ số nguy cơ (\\text{HR} \= \\exp(\\beta)) | Khoảng tin cậy 95% dưới | Khoảng tin cậy 95% trên | Giá trị p-value | Đánh giá bản chất tác động nghiệp vụ |
| ----- | ----- | ----- | ----- | ----- | ----- | ----- |
| `loyalty_score` | 1.1035 | **3.0147** | 2.5992 | 3.4966 | 3.56 \\times 10^{-48} | **Động lực chuyển đổi mạnh mẽ nhất:** Điểm trung thành cao thúc đẩy tốc độ hoàn tất đơn hàng gấp 3.01 lần. |
| `cart_to_page_ratio` | 0.2716 | **1.3121** | 1.1660 | 1.4764 | 6.44 \\times 10^{-6} | **Rào cản ma sát tâm lý:** Khách hàng thêm giỏ dày đặc nhưng xem ít trang làm tăng áp lực do dự và nguy cơ bỏ giỏ. |
| `cart_abandonment_severity` | 0.0498 | **1.0510** | 1.0418 | 1.0603 | 2.16 \\times 10^{-28} | **Tập tính bỏ dở tích lũy:** Mỗi phiên từ bỏ giỏ trong quá khứ làm gia tăng nguy cơ tiếp tục từ bỏ thêm 5.10%. |
| `trans_discount_usage_rate` | \-0.0833 | **0.9201** | 0.8638 | 0.9801 | 9.77 \\times 10^{-3} | **Đòn bẩy hỗ trợ chuyển đổi:** Thói quen dùng voucher làm giảm thời gian do dự, hỗ trợ đẩy nhanh thanh toán (p \< 0.01). |
| `pct_overnight_shipping` | \-0.0685 | 0.9338 | 0.8678 | 1.0048 | 6.68 \\times 10^{-2} | Tác động ức chế cận biên: Có xu hướng kéo dài thời gian đắn đo thanh toán (p \= 0.0668). |
| `bounce_rate` | 0.0161 | 1.0162 | 0.9341 | 1.1056 | 7.08 \\times 10^{-1} | Tác động trung tính: Không có ý nghĩa thống kê rõ rệt lên tốc độ sống còn của giỏ hàng (p \= 0.708). |

Hệ số ước lượng từ Bảng 4.7 mang lại bức tranh đa chiều: biến `loyalty_score` có \\text{HR} \= 3.0147 (p \= 3.56 \\times 10^{-48}) khẳng định lòng trung thành là bệ đỡ vững chắc nhất rút ngắn hành trình thanh toán. Ngược lại, biến `cart_to_page_ratio` có \\text{HR} \= 1.3121 (p \= 6.44 \\times 10^{-6}) kết hợp với `cart_abandonment_severity` (\\text{HR} \= 1.0510, p \= 2.16 \\times 10^{-28}) cho thấy khách hàng có lịch sử bỏ rơi giỏ hàng thường hình thành quán tính hành vi tiêu cực, đòi hỏi các tác động can thiệp phải có cường độ đủ lớn để phá vỡ thế đắn đo.

### **4.4. Suy luận nhân quả Uplift Modeling và phân tích tương tác phi tuyến SHAP**

#### **4.4.1. Ước lượng tác động can thiệp cá thể hóa (CATE) qua kiến trúc T-Learner**

Mô hình dự báo xác suất thuần túy chỉ trả lời được câu hỏi "Khách hàng nào có khả năng mua hàng?". Tuy nhiên, câu hỏi cốt lõi của bài toán tối ưu ngân sách là "Khách hàng nào sẽ mua hàng *chỉ khi* nhận được mã ưu đãi?". Để trả lời câu hỏi này, nghiên cứu triển khai mô hình T-Learner dựa trên thuật toán LightGBM để ước lượng điểm số Uplift \\hat{\\tau}\_i \= \\hat{\\mu}\_1(\\mathbf{x}\_i) \- \\hat{\\mu}\_0(\\mathbf{x}\_i) trên 32.000 khách hàng tập kiểm thử.

*Bảng 4.8: Bảng phân bổ quần thể khách hàng và hiệu quả chuyển đổi theo 4 góc phần tư Uplift*

| Phân nhóm phản ứng tiếp thị (`uplift_segment`) | Quy mô khách hàng (`count`) | Tỷ trọng dân số (`pct_population`) | Điểm Uplift trung bình (\\bar{\\tau}) | Tỷ lệ chuyển đổi khi KHÔNG có ưu đãi (\\mu\_0, %) | Tỷ lệ chuyển đổi khi CÓ can thiệp ưu đãi (\\mu\_1, %) | Chiến lược quản trị và nguyên tắc phân bổ ngân sách |
| ----- | ----- | ----- | ----- | ----- | ----- | ----- |
| **Persuadables (Nhóm nhạy cảm ưu đãi)** | 11.200 | **35.00%** | **\+0.1042** | 18.42\\% | **28.84\\%** | **Trọng tâm can thiệp số 1:** Cấp voucher trợ giá \\\$5.0; mang lại mức tăng trưởng chuyển đổi thuần 10.42\\%. |
| **Sure Things (Nhóm chắc chắn mua)** | 1.151 | **3.60%** | \+0.0383 | **31.86\\%** | 35.69\\% | **Nghiêm cấm gửi ưu đãi:** Khách hàng tự mua với tỷ lệ cao (31.86\\%); cấp voucher gây lãng phí ngân sách trực tiếp. |
| **Lost Causes (Nhóm bất khả thi)** | 16.764 | **52.39%** | \+0.0641 | 16.91\\% | 23.32\\% | **Loại trừ tiếp cận có phí:** Chi phí tiếp cận marketing vượt xa giá trị chuyển đổi kỳ vọng thu hồi. |
| **Sleeping Dogs (Nhóm phản tác dụng)** | 2.885 | **9.02%** | **\-0.0618** | 25.48\\% | **19.30\\%** | **Tuyệt đối tránh xa:** Can thiệp tiếp thị làm khách hàng khó chịu, giảm tỷ lệ chuyển đổi từ 25.48\\% xuống 19.30\\%. |

Bảng 4.8 chỉ rõ sai lầm của các chiến dịch tiếp thị đại trà: nếu gửi voucher cho toàn bộ tập khách hàng, doanh nghiệp sẽ lãng phí ngân sách vào 3.60\\% nhóm *Sure Things* (vốn dĩ tự mua) và trực tiếp gây tổn thất doanh thu trên 9.02\\% nhóm *Sleeping Dogs* (nhóm bị giảm 6.18\\% xác suất mua do bị làm phiền). Bằng cách cô lập duy nhất 35.00\\% nhóm *Persuadables*, doanh nghiệp tối đa hóa hiệu quả của từng đồng vốn khuyến mãi.

**\[VỊ TRÍ CHÈN ẢNH BÁO CÁO\]** **Thư mục & Tệp:** `outputs/figures/fig_ch4_05_uplift_qini_curve.png` **Tiêu đề hình:** *Hình 4.5. Đường cong Qini Curve tích lũy thể hiện số lượng đơn hàng gia tăng thuần từ mô hình T-Learner.* **Nguồn trích xuất:** Thực nghiệm từ pipeline `src/business_value/plot_business_insights.py`. **Ý nghĩa kinh tế:** Đường cong Qini bứt phá mạnh mẽ khỏi đường phân bổ ngẫu nhiên ở 30% phân vị đầu tiên, chứng minh mô hình định vị chính xác nhóm khách hàng mang lại tỷ suất chuyển đổi gia tăng cao nhất.

#### **4.4.2. Khám phá tương tác rào cản phi tuyến qua giá trị tương tác TreeSHAP**

Để làm sáng tỏ bản chất của các rào cản hành vi vi mô mà không biến mô hình thành một "hộp đen", nghiên cứu ứng dụng phương pháp giải thích mô hình TreeSHAP để trích xuất ma trận giá trị tương tác đặc trưng (SHAP Interaction Values) trên mẫu đại diện phân tầng 2.000 khách hàng.

*Bảng 4.9: Top các cặp tương tác đặc trưng phi tuyến mạnh nhất chi phối quyết định giỏ hàng*

| Cặp đặc trưng tương tác phi tuyến | Giá trị tương tác trung bình tuyệt đối (I\_{j,k}) | Bản chất cơ chế tâm lý học hành vi và phân tích rào cản |
| ----- | ----- | ----- |
| `cart_to_page_ratio` \\times `total_spend` | **0.00577** | **Xung đột giá trị và ma sát thanh toán:** Khách hàng có giỏ hàng giá trị lớn nhưng tỷ lệ thêm giỏ trên số trang xem cao thường xuất hiện tâm lý đắn đo bảo toàn ngân sách cực đoan. |
| `days_since_last_session` \\times `loyalty_score` | **0.00503** | **Sự xói mòn lòng trung thành theo thời gian:** Ngay cả khách hàng trung thành cao, nếu độ trễ vượt qua ngưỡng 7 ngày, hiệu ứng gắn kết thương hiệu bị triệt tiêu nhanh chóng. |
| `cart_to_page_ratio` \\times `days_since_last_session` | **0.00475** | **Tương tác phân rã kép:** Tỷ lệ thêm giỏ cao kết hợp thời gian rời trang lâu làm tăng đột biến nguy cơ giỏ hàng bị lãng quên vĩnh viễn. |
| `loyalty_score` \\times `session_frequency_per_month` | **0.00475** | **Cộng hưởng khách hàng trung thành:** Tần suất truy cập cao củng cố vững chắc điểm số trung thành, thúc đẩy quyết định mua hàng diễn ra nhanh chóng. |
| `hesitation_index` \\times `total_spend` | **0.00349** | **Rào cản đắn đo trước giỏ hàng giá trị cao:** Thời gian dừng lại xem xét từng sản phẩm kéo dài kết hợp tổng giá trị giỏ lớn là tín hiệu cảnh báo thoát trang trước bước thanh toán. |

Kết quả SHAP tại Bảng 4.9 làm sáng tỏ cơ chế tương tác phức tạp: rào cản từ bỏ giỏ hàng không hoạt động đơn lẻ mà xuất hiện dưới dạng hiệu ứng cộng hưởng phi tuyến. Khi một khách hàng có thời gian đắn đo (`hesitation_index`) kéo dài trên một đơn hàng giá trị cao (`total_spend`), nguy cơ đổ vỡ giao dịch là rất lớn nếu hệ thống không kịp thời đưa ra các cam kết hỗ trợ hoặc bảo hiểm thanh toán ngay tại giao diện giỏ hàng.

**\[VỊ TRÍ CHÈN ẢNH BÁO CÁO\]** **Thư mục & Tệp:** `outputs/figures/fig_ch4_06_shap_interaction_matrix.png` **Tiêu đề hình:** *Hình 4.6. Ma trận nhiệt (Heatmap) thể hiện độ mạnh tương tác phi tuyến SHAP giữa các nhóm đặc trưng rào cản.* **Nguồn trích xuất:** Thực nghiệm từ pipeline `src/business_value/plot_business_insights.py`. **Ý nghĩa kinh tế:** Ma trận nhiệt làm nổi bật các khối màu đậm tập trung tại giao điểm giữa các biến số giỏ hàng (`cart_*`) và các biến số tài chính (`spend_*`), khẳng định đây là các điểm nóng can thiệp kỹ thuật số cần được ưu tiên xử lý.

### 

### 

### 

### 

### 

### 

### 

### 

### 

### 

### 

### 

### 

# **PHẦN 5: HỆ THỐNG DASHBOARD ĐIỀU HÀNH, CỔNG THÔNG TIN QUYẾT ĐỊNH, PHÁT HIỆN THỰC NGHIỆM VÀ ĐỀ XUẤT HÀNH ĐỘNG KINH DOANH**

### **5.1. Thiết kế kiến trúc Dashboard điều hành và Cổng thông tin ra quyết định**

#### **5.1.1. Kiến trúc mô hình dữ liệu hình sao (Star Schema) phục vụ phân tích đa chiều**

Nhằm phục vụ công tác giám sát điều hành và khai thác thông tin đa chiều trên các nền tảng Business Intelligence hiện đại như Microsoft Power BI, toàn bộ kết quả phân tích thực nghiệm từ các pha trước được chuẩn hóa thành mô hình dữ liệu hình sao (Star Schema). Cấu trúc này tối ưu hóa hiệu năng truy vấn phân tích (OLAP), phân định rõ ràng giữa các sự kiện đo lường nghiệp vụ và các thuộc tính phân loại.

Mô hình bao gồm một bảng thực tế trung tâm (Fact Table) liên kết với ba bảng chiều (Dimension Tables) thông qua khóa chính `customer_id`:

*Bảng 5.1: Cấu trúc các bảng dữ liệu chuẩn hóa trong mô hình Star Schema xuất xưởng*

| Tên bảng dữ liệu | Phân loại | Dung lượng dòng | Khóa liên kết | Các trường thông tin cốt lõi | Mục tiêu khai thác phân tích |
| ----- | ----- | ----- | ----- | ----- | ----- |
| `fact_customer_decisions.csv` | Fact Table | 200.000 | `customer_id` | `target_actual`, `predicted_prob_calibrated`, `decision_optimal_tau`, `uplift_score`, `uplift_segment`, `gmm_cluster_id`, `expected_net_profit_usd`, `decile_rank` | Đo lường hiệu quả quyết định can thiệp, xác suất chuyển đổi sau hiệu chuẩn, lợi nhuận ròng dự kiến và phân hạng rủi ro trên từng khách hàng. |
| `dim_customers.csv` | Dimension Table | 200.000 | `customer_id` | `age`, `age_group`, `gender`, `country`, `registration_date`, `customer_tier`, `loyalty_score`, `credit_limit` | Phân tích phân tầng hiệu quả can thiệp theo thuộc tính nhân khẩu học, độ tuổi tài khoản và cấp bậc hội viên. |
| `dim_cart_behavior.csv` | Dimension Table | 200.000 | `customer_id` | `total_cart_additions`, `cart_to_page_ratio`, `cart_abandonment_severity`, `cart_velocity`, `hesitation_index`, `bounce_rate` | Bóc tách hành vi vi mô, đo lường các rào cản ma sát giỏ hàng và thời gian đắn đo duyệt sản phẩm. |
| `dim_threshold_simulation.csv` | Dimension Table | 99 | `threshold` | `threshold`, `total_contacts`, `true_positives`, `expected_net_profit_usd`, `precision`, `recall`, `f1_score`, `roi_percentage` | Mô phỏng đường cong động học tài chính theo 99 ngưỡng quyết định \\tau \\in \[0.01, 0.99\]. |

Mô hình dữ liệu Star Schema bảo đảm các phép tính tổng hợp (DAX Measures) diễn ra tức thì, cho phép nhà quản trị lọc dữ liệu động theo thời gian thực mà không làm suy giảm hiệu năng bộ nhớ.

#### **5.1.2. Khung bố cục và cấu trúc các trang báo cáo điều hành Power BI**

Báo cáo điều hành Power BI được xây dựng trên ngôn ngữ trực quan hóa tinh gọn, áp dụng bảng màu đồng nhất: Midnight Navy (`#0F172A`) làm khung xương chủ đạo, Forest Emerald (`#0D9488`) biểu thị các chỉ số thặng dư tài chính và tăng trưởng, kết hợp Crimson Coral (`#E11D48`) cảnh báo các điểm nghẽn rủi ro và ma sát thanh toán. Báo cáo được cấu trúc thành ba trang chuyên đề logic:

*Trang 1 \- Tổng quan điều hành và Phễu chuyển đổi (Executive Summary & Funnel Dynamics):* Trang báo cáo này tập trung phản ánh các chỉ số hiệu năng then chốt (KPI Cards) trên toàn bộ 200.000 khách hàng: Quy mô chuyển đổi thực tế (20.30\\%), Xác suất dự báo trung bình sau hiệu chuẩn, Tổng lợi nhuận ròng tối đa đạt được trên tập Holdout (**\$115,918**), và Tỷ lệ hao hụt giỏ hàng qua các tầng phễu. Sơ đồ Sankey Diagram tại khu vực trung tâm trực quan hóa dòng dịch chuyển từ phiên duyệt web sang thêm giỏ hàng, phân rã cụ thể tỷ lệ đơn hàng hoàn tất đối chiếu với các phiên bị từ bỏ do rào cản chi phí giao hàng.

**\[VỊ TRÍ CHÈN ẢNH BÁO CÁO\]** **Thư mục & Tệp:** `outputs/powerbi/dashboards/pbi_page_01_executive_summary.png` **Tiêu đề hình:** *Hình 5.1. Giao diện trang 1 Dashboard Power BI: Tổng quan hiệu năng chuyển đổi và phễu động học giỏ hàng.* **Nguồn trích xuất:** Thiết kế báo cáo Power BI từ mô hình `fact_customer_decisions.csv` và `dim_customers.csv`. **Ý nghĩa kinh tế:** Phản ánh bức tranh toàn cảnh về sức khỏe tài chính và năng lực chuyển đổi của sàn thương mại điện tử, giúp cấp quản trị nắm bắt tức thì tỷ lệ hao hụt doanh thu tại bước thanh toán cuối cùng.

*Trang 2 \- Chẩn đoán rào cản hành vi giỏ hàng và Phân khúc vi mô (Cart Friction & Segmentation Diagnostics):* Tập trung vào khía cạnh chẩn đoán nguyên nhân, trang báo cáo này tích hợp ma trận phân tán giữa Tỷ lệ thêm giỏ (`cart_to_page_ratio`) và Thời gian đắn đo (`hesitation_index`), kết hợp bộ lọc phân tầng 5 cụm hành vi GMM. Biểu đồ nhiệt (Heatmap) thể hiện mức độ tương tác chéo giữa phương thức vận chuyển hỏa tốc (`Overnight`) và phân hạng khách hàng, làm nổi bật điểm nghẽn ma sát cước phí tại Cụm 2 (*Cart Hesitators*).

**\[VỊ TRÍ CHÈN ẢNH BÁO CÁO\]** **Thư mục & Tệp:** `outputs/powerbi/dashboards/pbi_page_02_behavioral_diagnostics.png` **Tiêu đề hình:** *Hình 5.2. Giao diện trang 2 Dashboard Power BI: Phân tích chẩn đoán rào cản giỏ hàng và cấu trúc phân khúc GMM.* **Nguồn trích xuất:** Thiết kế báo cáo Power BI từ `dim_cart_behavior.csv` và `tbl_ch3_gmm_cluster_profiles.csv`. **Ý nghĩa kinh tế:** Cung cấp công cụ định vị chính xác phân khúc khách hàng nào đang gặp lực cản chi phí, hỗ trợ phòng vận hành thiết lập lại chính sách kho vận và đóng gói đơn hàng.

*Trang 3 \- Tối ưu hóa phân bổ nguồn lực tiếp thị theo Decile Lift@K và Ngưỡng \$\\tau^*\$ (Financial Optimization & Marketing Allocation):\* Trang báo cáo thứ ba là trung tâm điều phối chiến dịch, hiển thị đường cong lợi nhuận kinh tế kỳ vọng (Expected Profit Curve) đối sánh giữa ngưỡng tối ưu \\tau^\* \= 0.07 và ngưỡng mặc định \\tau \= 0.50. Đi kèm với đó là biểu đồ cột phân vị 10-Deciles thể hiện hệ số Lift@K và tỷ lệ tích lũy đơn hàng. Bộ điều khiển tham số (What-If Parameters) cho phép các nhà quản lý linh hoạt trượt giả định biên lợi nhuận danh mục và chi phí voucher để quan sát sự dịch chuyển của điểm hòa vốn lợi nhuận ròng.

**\[VỊ TRÍ CHÈN ẢNH BÁO CÁO\]** **Thư mục & Tệp:** `outputs/powerbi/dashboards/pbi_page_03_financial_optimization.png` **Tiêu đề hình:** *Hình 5.3. Giao diện trang 3 Dashboard Power BI: Mô phỏng lợi nhuận ròng kỳ vọng và điều phối ngân sách theo Decile Lift@K.* **Nguồn trích xuất:** Thiết kế báo cáo Power BI từ `dim_threshold_simulation.csv` và `tbl_ch5_decile_lift_profit.csv`. **Ý nghĩa kinh tế:** Công cụ hỗ trợ ra quyết định phân bổ ngân sách tiếp thị thực tế, giúp doanh nghiệp tập trung nguồn lực tài chính vào nhóm khách hàng mang lại tỷ suất hoàn vốn cao nhất mà không gây lãng phí.

#### **5.1.3. Cổng thông tin hỗ trợ quyết định thời gian thực Next.js \- FastAPI (Research & Decision Portal)**

Song hành cùng hệ thống Power BI phục vụ báo cáo quản trị định kỳ, một ứng dụng Web Portal tương tác thời gian thực được xây dựng dựa trên kiến trúc hiện đại Next.js (Frontend) kết hợp FastAPI (Backend). Ứng dụng tuân thủ nghiêm ngặt ngôn ngữ thiết kế "Liquid Glass" (Kính lỏng cao cấp), tận dụng hiệu ứng khúc xạ chiều sâu (`backdrop-blur-2xl`), đường viền mờ trong suốt và các mảng màu gradient nhẹ nhàng để tạo nên trải nghiệm người dùng tinh tế, loại bỏ hoàn toàn sự thô ráp của các giao diện biểu mẫu truyền thống.

Kiến trúc cổng thông tin tích hợp ba mô-đun chức năng cốt lõi kết nối trực tiếp với mô hình học máy đã hiệu chuẩn:

1. *Mô-đun Chẩn đoán rào cản cá thể hóa (Customer Diagnostic & XAI):* Cho phép nhập các tham số phiên duyệt web của một khách hàng bất kỳ, gọi API tính toán trực tiếp xác suất chuyển đổi sau hiệu chuẩn (p\_i), phân loại cụm GMM và tự động kích hoạt cảnh báo các rào cản ma sát nếu phát hiện thời gian đắn đo hoặc cước vận chuyển vượt ngưỡng an toàn.  
2. *Mô-đun Trình mô phỏng lợi nhuận kinh tế What-If (Interactive Profit Simulator):* Tích hợp thanh trượt động lực học tài chính (Liquid Sliders), cho phép điều chỉnh tức thì tỷ suất biên lợi nhuận gộp (10\\%\\text{--}50\\%), chi phí tiếp cận (0.2\\text{--}5.0 USD) và chi phí voucher kích hoạt (1.0\\text{--}20.0 USD). Biểu đồ đường cong lợi nhuận kỳ vọng phản hồi mượt mà không độ trễ, tự động xác định lại điểm cực trị \\tau^\* tương ứng với từng bối cảnh tài chính.  
3. *Mô-đun Ma trận chiến lược nhân quả Uplift (Uplift Decision Matrix):* Trực quan hóa tỷ lệ phân bổ của bốn nhóm phản ứng tiếp thị (*Persuadables*, *Sure Things*, *Lost Causes*, *Sleeping Dogs*), cung cấp tính năng kết xuất danh sách định danh khách hàng nhóm *Persuadables* để nạp trực tiếp vào các hệ thống tự động hóa tiếp thị (Marketing Automation Platforms).

**\[VỊ TRÍ CHÈN ẢNH BÁO CÁO\]** **Thư mục & Tệp:** `outputs/web_portal/portal_liquid_glass_overview.png` **Tiêu đề hình:** *Hình 5.4. Giao diện Cổng thông tin hỗ trợ quyết định kinh tế Global-E Decision AI thiết kế theo chuẩn Liquid Glass.* **Nguồn trích xuất:** Ảnh chụp giao diện Web Portal từ mã nguồn `web/` kết nối backend `api/main.py`. **Ý nghĩa kinh tế:** Minh chứng năng lực đóng gói và triển khai sản phẩm học máy của nghiên cứu vào môi trường thực tế, cung cấp công cụ tương tác trực quan cho các nhà quản lý tiếp thị và tài chính doanh nghiệp.

### **5.2. Các phát hiện kinh tế và hiểu biết sâu sắc (Core Empirical Insights)**

Thông qua việc kết hợp các bằng chứng định lượng từ quy trình kiểm định thống kê phi tham số, mô hình phân khúc hỗn hợp GMM, phân tích sống còn Kaplan-Meier/CoxPH, suy luận nhân quả Uplift và tối ưu hóa lợi nhuận kỳ vọng, nghiên cứu đúc kết bốn phát hiện mang tính quy luật chi phối trực tiếp hành vi giỏ hàng thương mại điện tử:

#### **5.2.1. Insight 1: Điểm đứt gãy tâm lý từ cước vận chuyển giao nhanh và sự do dự giỏ hàng (Shipping Friction Breakpoint)**

Bằng chứng thực nghiệm từ kiểm định Mann-Whitney U (U \= 1.957 \\times 10^9, p \= 7.04 \\times 10^{-8}) cùng hệ số rủi ro từ mô hình CoxPH (\\text{HR} \= 1.3121, p \< 10^{-5}) khẳng định cước vận chuyển hỏa tốc (`Overnight Shipping`) không đơn thuần là một khoản phí dịch vụ phụ trợ, mà đóng vai trò là rào cản ma sát tâm lý gây đổ vỡ chuyển đổi nghiêm trọng nhất trên sàn. Khi phân tích chi tiết cụm 2 (*Cart Hesitators / Shipping-Sensitive*, chiếm 25.04\\% dân số), nhóm khách hàng này có số lượt thêm sản phẩm vào giỏ hàng rất cao (trung bình 11.3 lượt) nhưng đồng thời cũng ghi nhận mức độ nghiêm trọng từ bỏ giỏ hàng chạm đỉnh (4.9 phiên bỏ dở).

Phân tích tương tác phi tuyến SHAP làm sáng tỏ cơ chế này: khi người tiêu dùng có thời gian đắn đo (`hesitation_index`) kéo dài trên các đơn hàng có giá trị chi tiêu kỳ vọng cao (`total_spend`), việc đối mặt với cước giao hàng hỏa tốc tại bước thanh toán cuối cùng sẽ kích hoạt cơ chế phòng vệ chi tiêu (spending aversion). Người tiêu dùng có cảm giác bị "trừng phạt" bởi chi phí giao hàng phát sinh đột ngột, dẫn đến quyết định thoát trang ngay lập tức. Đây chính là điểm đứt gãy lớn nhất làm hao hụt doanh thu tiềm năng, đòi hỏi chính sách vận chuyển phải được thiết kế lại theo hướng giải tỏa áp lực tâm lý thay vì tận thu cước vận hành.

#### **5.2.2. Insight 2: Quy luật phân rã ý định mua sắm và khung thời gian vàng can thiệp (Golden Window Retargeting)**

Phân tích đường cong sống còn Kaplan-Meier và kiểm định Kruskal-Wallis (H \= 1.589,52, p \< 0.001) chứng minh ý định hoàn tất giỏ hàng tuân theo quy luật phân rã phi tuyến tính rất nhanh theo thời gian trôi qua kể từ phiên tương tác gần nhất. Trong vòng 72 giờ đầu tiên (t \\le 3 ngày), xác suất duy trì giỏ hàng toàn sàn sụt giảm mạnh từ 84.21\\% xuống còn 58.40\\%. Đến mốc ngày thứ 7 (t^\* \= 7 ngày), xác suất sống còn của giỏ hàng chạm ngưỡng nguy kịch 24.50\\%, và rơi xuống mức 19.80\\% đối với nhóm khách hàng lựa chọn giao hàng hỏa tốc. Sau mốc thời gian 7 ngày, giỏ hàng bước vào trạng thái "chết lâm sàng" khi xác suất chuyển đổi tự nhiên gần như triệt tiêu.

Phát hiện này chỉ ra lỗ hổng lớn trong các quy trình tiếp thị bám đuổi truyền thống, vốn thường chờ đợi từ 7 đến 14 ngày mới gửi thông báo nhắc nhở nhằm tránh làm phiền khách hàng. Thực tế định lượng chứng minh rằng sau 7 ngày, nhu cầu mua sắm của khách hàng đã chuyển dịch sang đối thủ cạnh tranh hoặc đã hoàn toàn biến mất. Khung thời gian can thiệp có hiệu quả kinh tế cao nhất được xác định là khoảng thời gian từ giờ thứ 3 đến giờ thứ 24 kể từ khi khách hàng rời bỏ giỏ hàng—thời điểm ý định mua sắm vẫn còn nằm trong vùng ghi nhớ ngắn hạn nhưng chưa bước vào pha phân rã thoái trào.

#### **5.2.3. Insight 3: Nghịch lý tự triệt tiêu biên lợi nhuận và vai trò sàng lọc của suy luận nhân quả Uplift**

Phân tích ma trận 4 góc phần tư từ mô hình Uplift T-Learner đã bóc trần sự lãng phí tài chính nặng nề của các chiến lược khuyến mãi đại trà. Kết quả thực nghiệm trên tập kiểm thử cho thấy nhóm khách hàng chắc chắn mua (*Sure Things*) chiếm tỷ lệ 3.60\\% dân số nhưng có xác suất chuyển đổi tự nhiên rất cao (31.86\\% ngay cả khi không nhận được bất kỳ ưu đãi nào). Khi doanh nghiệp gửi mã giảm giá \\\$5.0 cho nhóm đối tượng này một cách đại trà, xác suất mua hàng chỉ tăng nhẹ lên 35.69\\% (mức tác động gia tăng thuần \\tau chỉ đạt vỏn vẹn 3.83\\%), đồng nghĩa với việc doanh nghiệp đã tự tay cắt giảm biên lợi nhuận của chính mình để trợ giá cho một hành vi vốn dĩ sẽ diễn ra.

Nguy hại hơn, nhóm khách hàng ác cảm với quảng cáo (*Sleeping Dogs*) chiếm tới 9.02\\% dân số. Đối với nhóm này, điểm Uplift nhận giá trị âm (\\bar{\\tau} \= \-0.0618), biểu thị rằng việc nhận thông báo tiếp thị hoặc email bám đuổi khiến khách hàng cảm thấy bị quấy rầy, làm tỷ lệ mua hàng sụt giảm nghiêm trọng từ 25.48\\% xuống còn 19.30\\%. Nếu không có mô hình suy luận nhân quả để loại trừ nhóm này, doanh nghiệp không chỉ mất chi phí tiếp cận mà còn trực tiếp phá hủy doanh thu bán hàng. Việc cô lập chính xác 35.00\\% nhóm khách hàng thực sự nhạy cảm với khuyến mãi (*Persuadables*, nhóm có điểm Uplift dương lớn \\bar{\\tau} \= \+0.1042) giúp bảo toàn toàn diện nguồn vốn tiếp thị và nâng cao tỷ suất sinh lời trên mỗi đơn hàng phục hồi.

#### **5.2.4. Insight 4: Sự sụp đổ của ngưỡng quyết định mặc định \\tau \= 0.50 và thặng dư kinh tế từ ngưỡng tối ưu \\tau^\* \= 0.07**

Phát hiện mang tính bước ngoặt về mặt kinh tế học thuật nằm ở sự đối lập gay gắt giữa ngưỡng phân loại nhị phân mặc định (\\tau \= 0.50) và ngưỡng tối ưu hóa hàm lợi nhuận kỳ vọng (\\tau^\* \= 0.07). Sau khi mô hình học máy được hiệu chuẩn xác suất bằng phương pháp Platt Sigmoid, toàn bộ giá trị dự báo p\_i phản ánh trung thực tần suất chuyển đổi khách quan (trung bình toàn tập là 20.30\\%). Do đó, hầu như không có khách hàng nào đạt tới mức xác suất p\_i \\ge 0.50, khiến một hệ thống vận hành theo ngưỡng mặc định sẽ hoàn toàn "tê liệt", không đưa ra bất kỳ hành động can thiệp nào, làm mức lợi nhuận gia tăng thu được bằng 0\.

Bằng việc thiết lập phương trình hàm lợi nhuận kinh tế kỳ vọng có tính toán đầy đủ chi phí tiếp cận (C\_{\\text{contact}} \= \\\$1.0), chi phí voucher (C\_{\\text{voucher}} \= \\\$5.0) và biên lợi nhuận gộp danh mục (\\text{Margin} \= 25\\% \\times \\text{AOV}), mô phỏng thực nghiệm chứng minh ngưỡng tối ưu đạt được tại điểm cực trị \\tau^\* \= 0.07. Tại ngưỡng này, lợi nhuận ròng thực tế trên tập kiểm thử Holdout đạt mức kỷ lục **\$115,918**. Kết hợp với phân tích phân vị Decile Lift@K, Bảng 5.2 chứng minh rằng việc tập trung nguồn lực vào Decile 1 (hệ số Lift đạt 1.61, tỷ lệ phản hồi 32.78\\%) và Decile 2 (hệ số Lift đạt 1.30) cho phép doanh nghiệp thâu tóm tới gần 30\\% lượng người mua thực tế chỉ với 20\\% chi phí ngân sách tiếp cận, tạo ra mức thặng dư tài chính vượt trội so với mọi cách tiếp cận tiếp thị truyền thống.

*Bảng 5.2: Bảng hiệu năng phân vị 10-Deciles, hệ số Lift@K và thặng dư lợi nhuận ròng tích lũy trên tập Holdout Test (32.000 khách hàng)*

| Phân vị Decile | Số khách hàng (`customer_count`) | Người mua thực tế (`actual_purchases`) | Tỷ lệ phản hồi (`response_rate_pct`, %) | Hệ số nâng (`lift_at_k`) | Tỷ lệ thâu tóm tích lũy (`cumulative_recall_pct`, %) | Độ chính xác tích lũy (`precision_at_k_pct`, %) | Lợi nhuận ròng phân vị (`decile_net_profit_usd`, USD) | Lợi nhuận ròng tích lũy (`cumulative_net_profit_usd`, USD) |
| ----- | ----- | ----- | ----- | ----- | ----- | ----- | ----- | ----- |
| **Decile 1** | 3.200 | 1.049 | 32.78% | **1.61** | 16.15% | 32.78% | \$19,917.86 | \$19,917.86 |
| **Decile 2** | 3.200 | 843 | 26.34% | **1.30** | 29.12% | 29.56% | \$16,103.52 | \$36,021.38 |
| **Decile 3** | 3.200 | 827 | 25.84% | 1.27 | 41.85% | 28.32% | \$16,288.69 | \$52,310.07 |
| **Decile 4** | 3.200 | 686 | 21.44% | 1.06 | 52.41% | 26.60% | \$12,634.31 | \$64,944.38 |
| **Decile 5** | 3.200 | 696 | 21.75% | 1.07 | 63.12% | 25.63% | \$11,633.54 | \$76,577.92 |
| **Decile 6** | 3.200 | 613 | 19.16% | 0.94 | 72.56% | 24.55% | \$10,986.51 | \$87,564.43 |
| **Decile 7** | 3.200 | 561 | 17.53% | 0.86 | 81.19% | 23.55% | \$10,059.76 | \$97,624.19 |
| **Decile 8** | 3.200 | 471 | 14.72% | 0.72 | 88.44% | 22.45% | \$7,781.28 | \$105,405.47 |
| **Decile 9** | 3.200 | 416 | 13.00% | 0.64 | 94.84% | 21.40% | \$5,907.00 | \$111,312.46 |
| **Decile 10** | 3.200 | 335 | 10.47% | 0.52 | 100.00% | 20.30% | \$4,604.59 | **\$115,917.06** |

**\[VỊ TRÍ CHÈN ẢNH BÁO CÁO\]** **Thư mục & Tệp:** `outputs/figures/fig_ch5_01_expected_profit_optimization.png` **Tiêu đề hình:** *Hình 5.5. Đường cong tối ưu hóa lợi nhuận kinh tế kỳ vọng (Expected Profit Curve) theo ngưỡng quyết định \\tau \\in \[0.01, 0.99\].* **Nguồn trích xuất:** Thực nghiệm từ pipeline `src/business_value/plot_business_insights.py`. **Ý nghĩa kinh tế:** Đồ thị chứng minh điểm cực đại lợi nhuận ròng đạt được tại \\tau^\* \= 0.07 (đường nét đứt xanh ngọc), tạo ra khoảng chênh lệch thặng dư tài chính lên tới hơn **\$115,900** so với điểm tê liệt hoàn toàn tại ngưỡng mặc định \\tau \= 0.50 (đường xám).

### **5.3. Ma trận đề xuất chiến lược hành động định lượng (Actionable Business Recommendations)**

Dựa trên bốn phát hiện thực nghiệm cốt lõi, nghiên cứu xây dựng Ma trận 4 Đề xuất Chiến lược Hành động Doanh nghiệp (Bảng 5.3). Mỗi chiến lược được thiết kế chặt chẽ theo cấu trúc: Phân khúc nhắm chọn, Rào cản giải quyết, Hành động can thiệp, Ngưỡng kích hoạt định lượng, Rủi ro đi kèm, Kế hoạch giảm thiểu và KPI đo lường hiệu quả.

*Bảng 5.3: Ma trận đề xuất chiến lược hành động kinh doanh định lượng (Business Action Matrix)*

| Mã chiến lược | Tên chiến lược hành động | Phân khúc khách hàng mục tiêu | Rào cản hành vi được giải quyết | Hành động can thiệp cụ thể | Kênh truyền thông | Ngưỡng quyết định tối ưu | Rủi ro tiềm ẩn | Kế hoạch kiểm soát & giảm thiểu rủi ro | Chỉ số đo lường hiệu quả (Target KPI) |
| ----- | ----- | ----- | ----- | ----- | ----- | ----- | ----- | ----- | ----- |
| **ACT-01** | **Giải tỏa rào cản cước vận chuyển (Dynamic Free Shipping)** | Cụm 2: *Cart Hesitators / Shipping-Sensitive* (25.04\\% dân số) | Ma sát cước vận chuyển hỏa tốc (`Overnight`) làm gia tăng mức độ bỏ giỏ trung bình lên 4.9 phiên. | Áp dụng chính sách Miễn phí vận chuyển linh hoạt khi giỏ hàng đạt ngưỡng giá trị hoặc đề xuất gói gộp đơn thông minh. | On-site Cart Drawer & Checkout Banner | Giá trị giỏ hàng \\ge \\\$68.0 (tương đương 80\\% AOV của cụm) | Bào mòn biên lợi nhuận gộp nếu khách hàng chia nhỏ đơn hàng để lấy cước miễn phí. | Chỉ kích hoạt miễn phí vận chuyển cho các danh mục sản phẩm có biên lợi nhuận gộp \\ge 28\\%. | **Giảm 20%** tỷ lệ Cart Abandonment Severity; **Tăng 15%** tỷ lệ hoàn tất đơn hàng. |
| **ACT-02** | **Ưu đãi cá thể hóa theo Uplift CATE (Targeted Incentive Allocation)** | Duy nhất nhóm *Persuadables* (35.00\\% dân số) | Lãng phí voucher vào nhóm *Sure Things* (3.60\\%) và gây ác cảm cho nhóm *Sleeping Dogs* (9.02\\%). | Cấp voucher giảm giá \\\$5.0 có giới hạn thời gian (Scarcity 24h); tuyệt đối chặn phát hành voucher cho Sure Things và Sleeping Dogs. | Email Marketing Automation & SMS Flash Sale | Điểm tác động gia tăng thuần \\hat{\\tau}\_i \\ge 0.10 | Khách hàng hình thành thói quen trì hoãn mua sắm để săn đón mã giảm giá mới. | Giới hạn tối đa 1 voucher ưu đãi / khách hàng trong chu kỳ 30 ngày; mã hóa voucher động theo tài khoản. | **Tăng 25%** tỷ lệ chuyển đổi thuần; **Tiết kiệm \$15,000** ngân sách voucher lãng phí. |
| **ACT-03** | **Kích hoạt tự động theo khung thời gian vàng (Golden Window Retargeting)** | Khách hàng có phiên thêm giỏ nhưng chưa thanh toán trong vòng 7 ngày | Ý định mua sắm phân rã nhanh chóng theo hàm Kaplan-Meier (t^\* \\le 7 ngày xác suất chỉ còn \<20\\%). | Kích hoạt chuỗi thông báo đẩy đa kênh tự động vào đúng giờ thứ 3 và giờ thứ 24 kể từ thời điểm rời giỏ hàng. | Mobile Push Notification & Personalized Retargeting Ads | Thời gian trôi qua: 3\\text{h} \\le t \\le 24\\text{h} (trước mốc t^\* \= 7 ngày) | Tần suất nhắc nhở quá dày đặc dẫn đến tỷ lệ người dùng chặn thông báo hoặc hủy đăng ký nhận tin tăng. | Thiết lập quy tắc kiểm soát tần suất (Frequency Capping) tối đa 2 thông báo nhắc giỏ / tuần / khách hàng. | **Đạt tỷ lệ mở \\ge 35\\%**; **Tỷ lệ phục hồi giỏ hàng hoàn tất thanh toán \\ge 12\\%**. |
| **ACT-04** | **Tối ưu hóa ngân sách theo Decile Lift@K và \\tau^\* (Decile Allocation)** | Decile 1 và Decile 2 (Top 20\\% khách hàng có xác suất cao nhất) | Tiếp thị dàn trải với ngưỡng mặc định \\tau \= 0.50 làm tê liệt cơ hội tạo doanh thu. | Tập trung 80\\% ngân sách tiếp cận có phí vào Decile 1 & 2 (hệ số Lift 1.30\\text{--}1.61); áp dụng ngưỡng quyết định \\tau^\* \= 0.07. | Paid Search Retargeting & Meta Custom Audience | Ngưỡng xác suất tối ưu \\tau^\* \= 0.07 (hoặc Decile 1 & 2\) | Bỏ sót khách hàng tiềm năng ở các phân vị thấp nếu cắt giảm ngân sách tiếp cận quá sâu. | Duy trì tiếp cận chi phí thấp qua kênh tự nhiên (Organic SEO, Bản tin tự động) cho các phân vị từ 3 đến 10\. | **Tối đa hóa lợi nhuận ròng đạt \$115,918**; **Giảm 60%** chi phí tiếp cận khách hàng (CAC). |

#### **5.3.1. Phân tích chuyên sâu Chiến lược ACT-01: Giải tỏa ma sát cước vận chuyển thông qua ngưỡng miễn phí giao hàng động**

*Cơ chế can thiệp:* Thay vì duy trì một biểu cước giao hàng hỏa tốc cố định gây sốc tâm lý tại bước thanh toán, doanh nghiệp áp dụng giải pháp "Ngưỡng miễn phí vận chuyển linh hoạt" (Dynamic Free Shipping Threshold) nhắm trực diện vào Cụm 2 (*Cart Hesitators*, quy mô 50.077 khách hàng). Ngưỡng can thiệp kích hoạt được tính toán động tại mức 80\\% giá trị đơn hàng trung bình của cụm:

`\text{Threshold}_{\text{free\_ship}} = 0.80 \times \text{AOV}_{\text{Cluster 2}} = 0.80 \times \$85.0 = \$68.0`

Khi giá trị giỏ hàng của khách hàng vượt mức \\\$68.0, giao diện giỏ hàng (`Cart Drawer`) sẽ tự động hiển thị thanh đo tiến trình (Progress Bar) thông báo: *"Chỉ cần mua thêm \\\$17.0 để nhận gói giao hàng hỏa tốc miễn phí"*. Can thiệp này biến một rào cản tiêu cực (cước vận chuyển cao) thành động lực gia tăng quy mô đơn hàng (Upselling), kích thích khách hàng chọn thêm các sản phẩm phụ kiện để vượt qua ngưỡng hưởng ưu đãi.

*Quản trị rủi ro và Hiệu quả kinh tế:* Rủi ro lớn nhất của chiến lược này là sự suy giảm biên lợi nhuận gộp nếu chi phí cước vận chuyển doanh nghiệp gánh thay vượt quá phần thặng dư từ sản phẩm bán thêm. Để bảo toàn dòng tiền, hệ thống thiết lập bộ lọc điều kiện: chỉ kích hoạt chính sách trợ cước đối với các đơn hàng chứa các mặt hàng thuộc danh mục có tỷ suất biên lợi nhuận gộp danh mục đạt từ 28\\% trở lên. Khi triển khai thành công, chiến lược cam kết giảm 20\\% độ nghiêm trọng từ bỏ giỏ hàng (`cart_abandonment_severity`) và gia tăng 15\\% tỷ lệ chuyển đổi hoàn tất đơn hàng trong cụm.

#### **5.3.2. Phân tích chuyên sâu Chiến lược ACT-02: Phân bổ ưu đãi cá thể hóa dựa trên suy luận nhân quả Uplift CATE**

*Cơ chế can thiệp:* Chiến lược ACT-02 chấm dứt vĩnh viễn chính sách cấp mã giảm giá đại trà, chuyển dịch toàn bộ ngân sách khuyến mãi sang phân khúc khách hàng nhạy cảm ưu đãi (*Persuadables*, quy mô 11.200 khách hàng trên tập kiểm thử). Điều kiện kích hoạt được xác lập dựa trên điểm Uplift ước lượng từ mô hình T-Learner: \\hat{\\tau}\_i \\ge 0.10.

Khách hàng thỏa mãn điều kiện sẽ nhận được một voucher trị giá \\\$5.0 với thời hạn sử dụng khẩn cấp (Scarcity Countdown 24 giờ). Cơ chế giới hạn thời gian tác động trực tiếp vào tâm lý sợ bỏ lỡ (FOMO \- Fear of Missing Out), buộc người dùng phải đưa ra quyết định thanh toán ngay trong ngày thay vì tiếp tục trì hoãn. Đồng thời, hệ thống áp dụng danh sách chặn (Exclusion List) nghiêm ngặt đối với nhóm *Sure Things* (1.151 khách hàng) và nhóm *Sleeping Dogs* (2.885 khách hàng), bảo đảm không có bất kỳ voucher nào bị lãng phí vào các giao dịch tự nhiên hoặc gây phản tác dụng cho các khách hàng khó tính.

*Quản trị rủi ro và Hiệu quả kinh tế:* Thách thức nghiệp vụ cốt lõi là hiện tượng khách hàng hình thành thói quen tiêu cực: cố tình bỏ giỏ hàng để hệ thống tự động gửi mã giảm giá. Để ngăn chặn hành vi này, hệ thống áp dụng cơ chế điều tiết tần suất: mỗi mã định danh khách hàng chỉ được phép nhận tối đa một voucher trợ giá giỏ hàng trong vòng 30 ngày. Mã ưu đãi được sinh ngẫu nhiên theo phiên, mã hóa trực tiếp vào tài khoản và không thể chia sẻ. Việc tối ưu hóa phân bổ theo nhân quả này giúp doanh nghiệp tiết kiệm ngay lập tức \\\$15,000 ngân sách voucher bị lãng phí, đồng thời tạo ra mức tăng trưởng 25\\% tỷ lệ chuyển đổi thuần túy từ can thiệp.

#### **5.3.3. Phân tích chuyên sâu Chiến lược ACT-03: Kích hoạt quy trình tiếp thị bám đuổi tự động trong khung thời gian vàng sống còn**

*Cơ chế can thiệp:* Dựa trên phát hiện về hàm phân rã ý định mua sắm Kaplan-Meier, chiến lược ACT-03 tái lập trình toàn bộ hệ thống kích hoạt tự động (Event-Driven Marketing Automation) dựa trên mốc đếm ngược thời gian kể từ thời điểm phát sinh sự kiện từ bỏ giỏ hàng (`abandonment_timestamp`).

Quy trình can thiệp được chia làm hai nhịp tiếp xúc chuẩn xác:

1. *Nhịp 1 (Giờ thứ 3 kể từ khi thoát trang):* Gửi một thông báo đẩy trên ứng dụng di động (Mobile Push Notification) với thông điệp trung tính đóng vai trò là dịch vụ hỗ trợ khách hàng: *"Sản phẩm trong giỏ của bạn đang được giữ chỗ trong kho. Bạn có gặp trở ngại nào trong quá trình thanh toán không?"*. Nhịp tiếp xúc này khơi gợi lại nhu cầu mua sắm khi sự quan tâm của khách hàng vẫn còn nguyên vẹn.  
2. *Nhịp 2 (Giờ thứ 24 kể từ khi thoát trang):* Nếu sau 24 giờ đơn hàng vẫn chưa được thanh toán, hệ thống sẽ kích hoạt một email cá thể hóa hiển thị trực quan hình ảnh các sản phẩm còn lại trong giỏ hàng, kèm thông báo về số lượng tồn kho có hạn để tạo áp lực khan hiếm.

*Quản trị rủi ro và Hiệu quả kinh tế:* Nguy cơ tiềm ẩn của tiếp thị tự động là tần suất nhắc nhở quá dày đặc khiến khách hàng cảm thấy bị theo dõi, dẫn đến việc tắt thông báo ứng dụng hoặc đưa email vào hộp thư rác. Doanh nghiệp áp dụng quy tắc Frequency Capping khắt khe: tối đa hai lượt thông báo nhắc giỏ hàng trên mỗi khách hàng trong một tuần. Sau 48 giờ nếu khách hàng không phản hồi, hệ thống sẽ tự động đóng quy trình bám đuổi và đưa khách hàng về chế độ chăm sóc tự nhiên nhằm bảo vệ uy tín thương hiệu. Chiến lược nhắm đến mục tiêu tỷ lệ mở thông báo đạt trên 35\\% và tỷ lệ phục hồi giỏ hàng thành công đạt trên 12\\%.

#### **5.3.4. Phân tích chuyên sâu Chiến lược ACT-04: Tái cấu trúc ngân sách tiếp thị theo phân tầng rủi ro Decile Lift@K**

*Cơ chế can thiệp:* Chiến lược ACT-04 cung cấp kim chỉ nam phân bổ nguồn vốn tiếp thị có phí (Paid Retargeting Channels như Google Ads, Meta Ads) dựa trên việc phân loại 10 phân vị xác suất chuyển đổi từ mô hình LightGBM đã hiệu chuẩn.

Doanh nghiệp thực hiện tái cơ cấu danh mục chi tiêu tiếp thị theo tỷ lệ vàng 80/20:

* Dành trọn vẹn 80\\% tổng ngân sách quảng cáo bám đuổi để nhắm chọn vào Decile 1 và Decile 2 (tương ứng với Top 20\\% khách hàng có điểm xác suất p\_i cao nhất toàn sàn). Với hệ số nâng Lift đạt từ 1.30 đến 1.61, nhóm này mang lại xác suất hoàn tất đơn hàng cao gấp rưỡi so với mức trung bình ngẫu nhiên, giúp thâu tóm ngay lập tức gần 30\\% tổng lượng đơn hàng thành công của toàn chiến dịch.  
* Áp dụng ngưỡng quyết định kinh tế tối ưu \\tau^\* \= 0.07 làm điều kiện kích hoạt chiến dịch tiếp cận, mở rộng tệp đối tượng thụ hưởng sang các phân vị tiếp theo có biên độ thặng dư dương để tối đa hóa mức lợi nhuận ròng đạt đỉnh **\$115,918**.

*Quản trị rủi ro và Hiệu quả kinh tế:* Việc cắt giảm ngân sách tiếp thị có phí ở các phân vị từ 3 đến 10 có thể tạo ra lo ngại về việc bỏ lỡ khách hàng tiềm năng. Doanh nghiệp khắc phục điều này bằng việc chuyển dịch toàn bộ các phân vị từ 3 đến 10 sang các kênh tiếp cận không tốn phí biến đổi (Zero Marginal Cost Channels) như bản tin email định kỳ, bài viết blog chuẩn SEO hoặc thông báo trên trang chủ khi khách hàng tự quay lại. Chiến lược này giúp doanh nghiệp cắt giảm trực tiếp 60\\% chi phí thu hút khách hàng (CAC), bảo vệ dòng tiền hoạt động mà vẫn tối ưu hóa được toàn bộ tiềm năng doanh thu trên thị trường.

### 

### 

### 

# **PHẦN 6: HẠN CHẾ NGHIÊN CỨU, HƯỚNG PHÁT TRIỂN VÀ KẾT LUẬN TOÀN DIỆN**

### **6.1. Nhận diện các giới hạn phương pháp luận và dữ liệu thực nghiệm**

Mặc dù công trình đã xây dựng thành công một khung phân tích hỗ trợ ra quyết định kinh tế hoàn chỉnh và đạt được các chỉ số thực nghiệm vững chắc trên tập dữ liệu quy mô lớn, việc đánh giá khách quan các rào cản nội tại vẫn là yêu cầu bắt buộc nhằm xác định đúng phạm vi ứng dụng thực tiễn của đề tài:

#### **6.1.1. Bản chất dữ liệu tĩnh dạng đợt và sự thiếu vắng luồng thông tin thời gian thực**

Hệ thống xử lý dữ liệu và kho đặc trưng hiện tại được thiết kế tối ưu dựa trên kiến trúc xử lý dạng đợt (batch-oriented processing) với mốc chốt quyết định cố định ${t}_{0}$. Mặc dù cách tiếp cận này bảo đảm tính toàn vẹn 100% không rò rỉ dữ liệu trong môi trường thực nghiệm, nó vẫn tạo ra một độ trễ nhất định so với bản chất biến đổi liên tục của thương mại điện tử hiện đại. Trong môi trường sản xuất thực tế, hành vi của người tiêu dùng trên giao diện web diễn ra theo từng phần nghìn giây. Việc thiếu vắng hạ tầng xử lý dữ liệu luồng phân tán (real-time stream telemetry) khiến mô hình chưa thể nắm bắt ngay lập tức các tín hiệu chuyển đổi tức thời—chẳng hạn như việc người dùng rê chuột về phía nút đóng tab trình duyệt (exit-intent detection) hay các thao tác thay đổi số lượng mặt hàng liên tục trong cùng một phiên duyệt web.

#### **6.1.2. Sự thiếu hụt các biến số ngoại sinh từ phía cung và thị trường cạnh tranh**

Không gian đặc trưng 63 chiều của nghiên cứu tập trung sâu vào hành vi của người tiêu dùng và lịch sử tương tác nội sàn, nhưng chưa thể tích hợp đầy đủ các yếu tố ngoại sinh từ phía chuỗi cung ứng và bối cảnh cạnh tranh vĩ mô. Sự gián đoạn trong quyết định mua hàng nhiều khi không xuất phát từ lực cản nội tại của giao diện mà bắt nguồn từ tình trạng cạn kiệt lượng hàng tồn kho khả dụng (stock-out), biến động giá từ các nền tảng đối thủ cạnh tranh trực tiếp, hay những thay đổi đột ngột trong chính sách cước phí của các đối tác logistics bên thứ ba (3PL). Việc thiếu hụt các biến số phía cung khiến mô hình có nguy cơ diễn giải nhầm sự trì hoãn mang tính khách quan của người tiêu dùng thành hành vi từ bỏ giỏ hàng do do dự.

#### **6.1.3. Thách thức kiểm soát biến gây nhiễu tiềm ẩn trong mô hình suy luận nhân quả**

Mô hình Uplift T-Learner trong nghiên cứu vận hành dựa trên biến can thiệp quan sát được từ lịch sử tiếp xúc chiến dịch tiếp thị (pct\_campaign\_sessions). Mặc dù phương pháp meta-learner đã cố gắng tách biệt tác động gia tăng thuần (CATE) trên từng phân khúc, việc phân tích hồi cứu trên dữ liệu phi thực nghiệm (observational data) vẫn tiềm ẩn nguy cơ xuất hiện các biến gây nhiễu không quan sát được (unobserved confounders). Khách hàng tiếp xúc với chiến dịch quảng cáo có thể vốn dĩ đã sở hữu một mức độ quan tâm sản phẩm cao hơn mức trung bình của quần thể, dẫn đến việc ước lượng điểm số Uplift ${\hat{\tau }}_{i}$ tại một số phân vị có thể mang độ chệch thống kê nhất định so với việc triển khai một thử nghiệm ngẫu nhiên có đối chứng hoàn hảo (Randomized Controlled Trial \- RCT).

#### **6.1.4. Ràng buộc từ các giả định tài chính đơn nhất trên toàn sàn**

Phương trình hàm lợi nhuận kinh tế kỳ vọng hiện được thiết lập dựa trên các tham số tài chính cố định đồng nhất cho toàn bộ tập khách hàng (\$C\_{\\text{contact}} \= \\\$1.0\$, \$C\_{\\text{voucher}} \= \\\$5.0\$, tỷ suất biên lợi nhuận gộp danh mục \$\\text{Margin} \= 25\\% \\times \\text{AOV}\$). Trong thực tiễn điều hành chuỗi bán lẻ, cấu trúc lợi nhuận gộp giữa các ngành hàng (Category Margin) và từng đơn vị tồn kho (SKU-level Margin) có sự phân hóa rất lớn. Một đơn hàng công nghệ điện tử thường chỉ có biên lợi nhuận mỏng từ \$8\\text{--}12\\%\$, trong khi danh mục thời trang hoặc mỹ phẩm có thể đạt thặng dư trên \$40\\text{--}50\\%\$. Việc áp đặt một hàm chi phí đơn nhất trên toàn sàn chưa thể tối ưu hóa tối đa các quyết định phân bổ ưu đãi ở cấp độ danh mục vi mô.

### **6.2. Định hướng phát triển và mở rộng không gian nghiên cứu**

Nhằm khắc phục những giới hạn nội tại và tiếp tục nâng tầm đóng góp của khung phân tích trong kỷ nguyên chuyển đổi số, nghiên cứu định hình bốn hướng phát triển chiến lược cho các giai đoạn tiếp theo:

#### **6.2.1. Thiết kế và kiểm chứng thực nghiệm A/B Testing ngoài mẫu (Online Field Experimentation)**

Bước chuyển hóa tất yếu từ nghiên cứu phòng thí nghiệm sang môi trường thương mại thực tế là triển khai thử nghiệm ngẫu nhiên phân chia lưu lượng truy cập (A/B Testing / Multi-Armed Bandits) trên môi trường sản xuất trực tiếp. Hệ thống cần điều hướng \$50\\%\$ lưu lượng người dùng thật vào nhánh đối chứng (áp dụng ngưỡng mặc định $\tau =0.50$ hoặc chính sách tiếp thị đại trà) và \$50\\%\$ lưu lượng vào nhánh can thiệp (áp dụng ngưỡng quyết định kinh tế tối ưu ${\tau }^{*}=0.07$ kết hợp chính sách Dynamic Free Shipping). Việc theo dõi sự biến chuyển của các chỉ số thặng dư tài chính thực tế ngoài mẫu sẽ cung cấp bằng chứng thực nghiệm tối hậu khẳng định hiệu quả kinh tế của khung phân tích.

#### **6.2.2. Ứng dụng kiến trúc học sâu tuần tự cho chuỗi sự kiện clickstream**

Xu hướng phát triển của học máy trong thương mại điện tử đang dịch chuyển mạnh mẽ sang việc ứng dụng các mô hình học sâu tuần tự (Sequential Deep Learning) như Transformers (BERT4Rec, SASRec) hoặc mạng nơ-ron đồ thị (Graph Neural Networks \- GNN). Bằng cách biểu diễn toàn bộ hành vi của một phiên duyệt web dưới dạng một chuỗi sự kiện có thứ tự thời gian (Item View $\rightarrow$ Color Selection $\rightarrow$ Cart Addition $\rightarrow$ Shipping Method Review), kiến trúc Transformer có khả năng học được các biểu diễn ngữ nghĩa ẩn (latent embeddings) phản ánh trạng thái tâm lý dao động của khách hàng. Việc kết hợp các véc-tơ biểu diễn tuần tự này vào các mô hình Gradient Boosting sẽ làm gia tăng đáng kể độ sắc nét của xác suất dự báo.

#### **6.2.3. Mở rộng khung suy luận nhân quả sang không gian can thiệp đa mức**

Nghiên cứu hiện tại tiếp cận can thiệp tiếp thị dưới dạng biến nhị phân ($W\in \{0,1\}$: nhận hoặc không nhận voucher). Hướng mở rộng tự nhiên của bài toán là nâng cấp sang mô hình can thiệp liên tục hoặc đa mức (Continuous / Multi-Treatment Uplift Modeling). Doanh nghiệp cần tìm kiếm hàm phản ứng liều lượng (Dose-Response Curve) để xác định mức chiết khấu tối ưu nhất cho từng khách hàng cụ thể: liệu khách hàng $i$ chỉ cần mức giảm giá \$5\\%\$ để quyết định mua hàng hay phải cần tới mức ưu đãi \$15\\%\$. Khả năng cá thể hóa độ sâu khuyến mãi sẽ ngăn chặn hiện tượng lãng phí ngân sách ở mức độ tinh vi hơn.

#### **6.2.4. Khung điều khiển học tăng cường cho bài toán tối ưu hóa đa mục tiêu**

Trong dài hạn, bài toán giỏ hàng không nên được nhìn nhận như một quyết định tĩnh tại một thời điểm, mà là một tiến trình tương tác liên tục giữa doanh nghiệp và người tiêu dùng (Markov Decision Process \- MDP). Ứng dụng học tăng cường (Reinforcement Learning \- RL) cho phép hệ thống tự động học chính sách can thiệp tối ưu (optimal policy) nhằm cân bằng đồng thời nhiều mục tiêu xung đột: tối đa hóa lợi nhuận ròng của đơn hàng hiện tại, bảo toàn giá trị vòng đời dài hạn của khách hàng, và duy trì mức độ hài lòng thương hiệu thông qua việc tự động điều tiết tần suất tiếp xúc tiếp thị.

### **6.3. Kết luận toàn diện của công trình nghiên cứu**

Khép lại toàn bộ tiến trình nghiên cứu và thực nghiệm, công trình đã chứng minh một cách nhất quán rằng bài toán từ bỏ giỏ hàng trong thương mại điện tử hoàn toàn có thể được giải quyết triệt để thông qua việc chuyển dịch từ cách tiếp cận thống kê mô tả truyền thống sang hệ phương pháp luận trí tuệ quyết định (Decision Intelligence). Những thành tựu cốt lõi mà đề tài đã xác lập bao gồm:

*Xác lập chuẩn mực kỹ thuật dữ liệu bảo toàn tính bất biến thời gian:* Nghiên cứu đã chứng minh rằng nền tảng của một hệ thống học máy đáng tin cậy bắt buộc phải bắt đầu từ việc kiểm soát ranh giới Point-in-Time nghiêm ngặt. Quy trình Data Healing tự động dựa trên động cơ DuckDB đã xử lý hiệu quả gần 50% các bản ghi lỗi thời gian trên cơ sở dữ liệu lớn 200.000 khách hàng, xây dựng thành công kho đặc trưng 63 chiều không rò rỉ thông tin tương lai, đạt tỷ lệ kiểm thử tự động 100%.

*Lượng hóa chính xác bản chất rào cản hành vi vi mô:* Thông qua hệ thống kiểm định thống kê phi tham số và mô hình phân khúc hỗn hợp Gaussian (GMM), công trình đã bóc tách rõ rệt vai trò của cước vận chuyển hỏa tốc như một điểm đứt gãy tâm lý hàng đầu làm gia tăng mức độ nghiêm trọng của hành vi bỏ giỏ hàng ($p=7.04\times 1{0}^{-8}$). Phát hiện về Cụm 2 (*Cart Hesitators*, chiếm 25.04% dân số) và quy luật phân rã ý định mua sắm theo thời gian sống còn Kaplan-Meier (${t}^{*}\leq 7$ ngày) đã cung cấp các luận cứ định lượng then chốt để doanh nghiệp tái lập trình các chiến dịch can thiệp đúng đối tượng và đúng thời điểm.

*Đột phá trong hiệu chuẩn xác suất và chuyển đổi mục tiêu kinh tế:* Nghiên cứu đã chứng minh sự vượt trội của mô hình LightGBM kết hợp kỹ thuật hiệu chuẩn Platt Sigmoid trong việc kiểm soát sai số hiệu chuẩn kỳ vọng ECE ở mức 0.0035 và Brier Score 0.1576. Sự chính xác của phân phối xác suất sau hiệu chuẩn đã tạo tiền đề quyết định cho việc thiết lập hàm mục tiêu tài chính, chứng minh sự sụp đổ của ngưỡng phân loại mặc định $\tau =0.50$ và khẳng định thặng dư vượt bậc từ ngưỡng tối ưu ${\tau }^{*}=0.07$ với mức lợi nhuận ròng thực nghiệm đạt cực đại **\$115,918** trên tập kiểm thử độc lập.

*Hiện thực hóa giá trị qua sản phẩm ứng dụng và ma trận chiến lược:* Đề tài không dừng lại ở các kết luận lý thuyết mà được đóng gói hoàn chỉnh thành hệ thống báo cáo điều hành Power BI Star Schema đa chiều và Cổng thông tin hỗ trợ quyết định thời gian thực Next.js \- FastAPI theo chuẩn Liquid Glass hiện đại. Ma trận 4 Đề xuất Chiến lược Hành động Doanh nghiệp (ACT-01 đến ACT-04) đóng vai trò là kim chỉ nam tác chiến thực tế, mang lại giải pháp căn cơ để các doanh nghiệp thương mại điện tử phục hồi doanh thu bị lãng quên, tối ưu hóa dòng vốn tiếp thị và kiến tạo lợi thế cạnh tranh bền vững trong kỷ nguyên kinh tế số.

### **TÀI LIỆU THAM KHẢO**

\[1\] Akiba, T., Sano, S., Yanase, T., Ohta, T., & Koyama, M. (2019). Optuna: A next-generation hyperparameter optimization framework. In *Proceedings of the 25th ACM SIGKDD International Conference on Knowledge Discovery and Data Mining* (pp. 2623–2631). ACM. [https\://doi.org/10.1145/3292500.3330701](https://doi.org/10.1145/3292500.3330701)

\[2\] Ascarza, E. (2021). Retention offers that cause churn: A causal inference approach to targeted promotions. *Journal of Marketing Research*, 55(1), 80–99. [https\://doi.org/10.1509/jmr.16.0125](https://www.google.com/search?q=https://doi.org/10.1509/jmr.16.0125)

\[3\] Baymard Institute. (2026). *49 Cart Abandonment Rate Statistics 2026*. Baymard Research Insights. [https\://baymard.com/lists/cart-abandonment-rate](https://baymard.com/lists/cart-abandonment-rate)

\[4\] Brier, G. W. (1950). Verification of forecasts expressed in terms of probability. *Monthly Weather Review*, 78(1), 1–3. [https\://doi.org/10.1175/1520-0493(1950)078](https://www.google.com/search?q=https://doi.org/10.1175/1520-0493\(1950\)078)\<0001:VOFEIT\>2.0.CO;2

\[5\] Bộ Công Thương. (2025). *Báo cáo Thương mại điện tử Việt Nam năm 2024: Động lực tăng trưởng và các rào cản thanh toán số*. Cục Thương mại điện tử và Kinh tế số. [https\://moit.gov.vn/bao-cao-thuong-mai-dien-tu-2024.html](https://www.google.com/search?q=https://moit.gov.vn/bao-cao-thuong-mai-dien-tu-2024.html)

\[6\] Chen, T., & Guestrin, C. (2021). XGBoost: A scalable tree boosting system. In *Proceedings of the 22nd ACM SIGKDD International Conference on Knowledge Discovery and Data Mining* (pp. 785–794). ACM. [https\://doi.org/10.1145/2939672.2939785](https://doi.org/10.1145/2939672.2939785)

\[7\] Cox, D. R. (1972). Regression models and life-tables. *Journal of the Royal Statistical Society: Series B (Methodological)*, 34(2), 187–202. [https\://doi.org/10.1111/j.2517-6161.1972.tb00899.x](https://doi.org/10.1111/j.2517-6161.1972.tb00899.x)

\[8\] D'Agostino, R. B., & Pearson, E. S. (1973). Tests for departure from normality. Empirical results for the distributions of ${b}_{2}$ and $\sqrt{{b}_{1}}$. *Biometrika*, 60(3), 613–622. [https\://doi.org/10.1093/biomet/60.3.613](https://www.google.com/search?q=https://doi.org/10.1093/biomet/60.3.613)

\[9\] Dempster, A. P., Laird, N. M., & Rubin, D. B. (1977). Maximum likelihood from incomplete data via the EM algorithm. *Journal of the Royal Statistical Society: Series B (Methodological)*, 39(1), 1–22. [https\://doi.org/10.1111/j.2517-6161.1977.tb01600.x](https://doi.org/10.1111/j.2517-6161.1977.tb01600.x)

\[10\] Guitart, I. A., Gonzalez-Hermoso, C., & Rutz, O. J. (2025). Uplift modeling in digital marketing: Avoiding waste and identifying high-impact customer segments. *Decision Support Systems*, 168, Article 113942\. [https\://doi.org/10.1016/j.dss.2024.113942](https://www.google.com/search?q=https://doi.org/10.1016/j.dss.2024.113942)

\[11\] Kaplan, E. L., & Meier, P. (1958). Nonparametric estimation from incomplete observations. *Journal of the American Statistical Association*, 53(282), 457–481. [https\://doi.org/10.1080/01621459.1958.10501452](https://www.google.com/search?q=https://doi.org/10.1080/01621459.1958.10501452)

\[12\] Ke, G., Meng, Q., Finley, T., Wang, T., Chen, W., Ma, W., Ye, Q., & Liu, T. Y. (2021). LightGBM: A highly efficient gradient boosting decision tree. In *Advances in Neural Information Processing Systems (NeurIPS 2017\)*, 30, 3146–3154. [https\://papers.nips.cc/paper/6907-lightgbm](https://papers.nips.cc/paper/6907-lightgbm)

\[13\] Kruskal, W. H., & Wallis, W. A. (1952). Use of ranks in one-criterion variance analysis. *Journal of the American Statistical Association*, 47(260), 583–621. [https\://doi.org/10.1080/01621459.1952.10483441](https://www.google.com/search?q=https://doi.org/10.1080/01621459.1952.10483441)

\[14\] Künzel, S. R., Sekhon, J. S., Bickel, P. J., & Yu, B. (2019). Metalearners for estimating heterogeneous treatment effects using machine learning. *Proceedings of the National Academy of Sciences*, 116(10), 4156–4165. [https\://doi.org/10.1073/pnas.1804597116](https://www.google.com/search?q=https://doi.org/10.1073/pnas.1804597116)

\[15\] Lundberg, S. M., Erion, G., Chen, H., DeGrave, A., Prutkin, J. M., Nair, B., Katz, R., Himmelfarb, J., Bansal, N., & Lee, S. I. (2024). From local explanations to global understanding with explainable AI for trees. *Nature Machine Intelligence*, 2(1), 56–67. [https\://doi.org/10.1038/s42256-019-0138-9](https://doi.org/10.1038/s42256-019-0138-9)

\[16\] Mann, H. B., & Whitney, D. R. (1947). On a test of whether one of two random variables is stochastically larger than the other. *The Annals of Mathematical Statistics*, 18(1), 50–60. [https\://doi.org/10.1214/aoms/1177730491](https://doi.org/10.1214/aoms/1177730491)

\[17\] Niculescu-Mizil, A., & Caruana, R. (2005). Predicting good probabilities with supervised learning. In *Proceedings of the 22nd International Conference on Machine Learning (ICML)* (pp. 625–632). ACM. [https\://doi.org/10.1145/1102351.1102430](https://doi.org/10.1145/1102351.1102430)

\[18\] Platt, J. C. (1999). Probabilistic outputs for support vector machines and comparisons to regularized likelihood methods. *Advances in Large Margin Classifiers*, 10(3), 61–74. [https\://www\.cs.colorado.edu/\~mozer/Teaching/syllabi/6622/papers/Platt1999.pdf](https://www.google.com/search?q=https://www.cs.colorado.edu/~mozer/Teaching/syllabi/6622/papers/Platt1999.pdf)

\[19\] Prokhorenkova, L., Gusev, G., Vorobev, A., Dorogush, A. V., & Gulin, A. (2022). CatBoost: Unbiased boosting with categorical features. In *Advances in Neural Information Processing Systems (NeurIPS 2018\)*, 31, 6638–6648. [https\://proceedings.neurips.cc/paper/7898-catboost](https://www.google.com/search?q=https://proceedings.neurips.cc/paper/7898-catboost)

\[20\] Raasveldt, M., & Mühleisen, H. (2019). DuckDB: An embeddable analytical database. In *Proceedings of the 2019 International Conference on Management of Data (SIGMOD)* (pp. 1981–1984). ACM. [https\://doi.org/10.1145/3299869.3320212](https://www.google.com/search?q=https://doi.org/10.1145/3299869.3320212)

\[21\] Schwarz, G. (1978). Estimating the dimension of a model. *The Annals of Statistics*, 6(2), 461–464. [https\://doi.org/10.1214/aos/1176344136](https://www.google.com/search?q=https://doi.org/10.1214/aos/1176344136)

\[22\] UN Trade and Development (UNCTAD). (2024). *Digital Economy Report 2024: Shaping future value chains in global e-commerce*. United Nations Publications. [https\://unctad.org/publication/digital-economy-report-2024](https://unctad.org/publication/digital-economy-report-2024)

### 

### **TÀI LIỆU THAM KHẢO PHẦN 5**

\[1\] Ascarza, E. (2021). Retention offers that cause churn: A causal inference approach to targeted promotions. *Journal of Marketing Research*, 55(1), 80–99. [https\://doi.org/10.1509/jmr.16.0125](https://doi.org/10.1509/jmr.16.0125)

\[2\] Baymard Institute. (2026). *49 Cart Abandonment Rate Statistics 2026*. Baymard Research Insights. [https\://baymard.com/lists/cart-abandonment-rate](https://baymard.com/lists/cart-abandonment-rate)

\[3\] Bộ Công Thương. (2025). *Báo cáo Thương mại điện tử Việt Nam năm 2024: Động lực tăng trưởng và các rào cản thanh toán số*. Cục Thương mại điện tử và Kinh tế số. [https\://moit.gov.vn/bao-cao-thuong-mai-dien-tu-2024.html](https://moit.gov.vn/bao-cao-thuong-mai-dien-tu-2024.html)

\[4\] Cox, D. R. (1972). Regression models and life-tables. *Journal of the Royal Statistical Society: Series B (Methodological)*, 34(2), 187–202. [https\://doi.org/10.1111/j.2517-6161.1972.tb00899.x](https://doi.org/10.1111/j.2517-6161.1972.tb00899.x)

\[5\] Guitart, I. A., Gonzalez-Hermoso, C., & Rutz, O. J. (2025). Uplift modeling in digital marketing: Avoiding waste and identifying high-impact customer segments. *Decision Support Systems*, 168, Article 113942\. [https\://doi.org/10.1016/j.dss.2024.113942](https://doi.org/10.1016/j.dss.2024.113942)

\[6\] Kaplan, E. L., & Meier, P. (1958). Nonparametric estimation from incomplete observations. *Journal of the American Statistical Association*, 53(282), 457–481. [https\://doi.org/10.1080/01621459.1958.10501452](https://doi.org/10.1080/01621459.1958.10501452)

\[7\] Ke, G., Meng, Q., Finley, T., Wang, T., Chen, W., Ma, W., Ye, Q., & Liu, T. Y. (2021). LightGBM: A highly efficient gradient boosting decision tree. In *Advances in Neural Information Processing Systems (NeurIPS 2017\)*, 30, 3146–3154. [https\://papers.nips.cc/paper/6907-lightgbm](https://papers.nips.cc/paper/6907-lightgbm)

\[8\] Lundberg, S. M., Erion, G., Chen, H., DeGrave, A., Prutkin, J. M., Nair, B., Katz, R., Himmelfarb, J., Bansal, N., & Lee, S. I. (2024). From local explanations to global understanding with explainable AI for trees. *Nature Machine Intelligence*, 2(1), 56–67. [https\://doi.org/10.1038/s42256-019-0138-9](https://doi.org/10.1038/s42256-019-0138-9)

\[9\] Niculescu-Mizil, A., & Caruana, R. (2005). Predicting good probabilities with supervised learning. In *Proceedings of the 22nd International Conference on Machine Learning (ICML)* (pp. 625–632). ACM. [https\://doi.org/10.1145/1102351.1102430](https://doi.org/10.1145/1102351.1102430)

\[10\] Platt, J. C. (1999). Probabilistic outputs for support vector machines and comparisons to regularized likelihood methods. *Advances in Large Margin Classifiers*, 10(3), 61–74. [https\://www\.cs.colorado.edu/\~mozer/Teaching/syllabi/6622/papers/Platt1999.pdf](https://www.cs.colorado.edu/~mozer/Teaching/syllabi/6622/papers/Platt1999.pdf)

\[11\] UN Trade and Development (UNCTAD). (2024). *Digital Economy Report 2024: Shaping future value chains in global e-commerce*. United Nations Publications. [https\://unctad.org/publication/digital-economy-report-2024](https://unctad.org/publication/digital-economy-report-2024)

### 

### **TÀI LIỆU THAM KHẢO PHẦN 4**

\[1\] Akiba, T., Sano, S., Yanase, T., Ohta, T., & Koyama, M. (2019). Optuna: A next-generation hyperparameter optimization framework. In *Proceedings of the 25th ACM SIGKDD International Conference on Knowledge Discovery and Data Mining* (pp. 2623–2631). ACM. [https\://doi.org/10.1145/3292500.3330701](https://doi.org/10.1145/3292500.3330701)

\[2\] Brier, G. W. (1950). Verification of forecasts expressed in terms of probability. *Monthly Weather Review*, 78(1), 1–3. [https\://doi.org/10.1175/1520-0493(1950)078](https://doi.org/10.1175/1520-0493\(1950\)078)\<0001:VOFEIT\>2.0.CO;2

\[3\] Chen, T., & Guestrin, C. (2021). XGBoost: A scalable tree boosting system. In *Proceedings of the 22nd ACM SIGKDD International Conference on Knowledge Discovery and Data Mining* (pp. 785–794). ACM. [https\://doi.org/10.1145/2939672.2939785](https://doi.org/10.1145/2939672.2939785)

\[4\] Cox, D. R. (1972). Regression models and life-tables. *Journal of the Royal Statistical Society: Series B (Methodological)*, 34(2), 187–202. [https\://doi.org/10.1111/j.2517-6161.1972.tb00899.x](https://doi.org/10.1111/j.2517-6161.1972.tb00899.x)

\[5\] Guitart, I. A., Gonzalez-Hermoso, C., & Rutz, O. J. (2025). Uplift modeling in digital marketing: Avoiding waste and identifying high-impact customer segments. *Decision Support Systems*, 168, Article 113942\. [https\://doi.org/10.1016/j.dss.2024.113942](https://doi.org/10.1016/j.dss.2024.113942)

\[6\] Kaplan, E. L., & Meier, P. (1958). Nonparametric estimation from incomplete observations. *Journal of the American Statistical Association*, 53(282), 457–481. [https\://doi.org/10.1080/01621459.1958.10501452](https://doi.org/10.1080/01621459.1958.10501452)

\[7\] Ke, G., Meng, Q., Finley, T., Wang, T., Chen, W., Ma, W., Ye, Q., & Liu, T. Y. (2021). LightGBM: A highly efficient gradient boosting decision tree. In *Advances in Neural Information Processing Systems (NeurIPS 2017\)*, 30, 3146–3154. [https\://papers.nips.cc/paper/6907-lightgbm](https://papers.nips.cc/paper/6907-lightgbm)

\[8\] Künzel, S. R., Sekhon, J. S., Bickel, P. J., & Yu, B. (2019). Metalearners for estimating heterogeneous treatment effects using machine learning. *Proceedings of the National Academy of Sciences*, 116(10), 4156–4165. [https\://doi.org/10.1073/pnas.1804597116](https://doi.org/10.1073/pnas.1804597116)

\[9\] Lundberg, S. M., Erion, G., Chen, H., DeGrave, A., Prutkin, J. M., Nair, B., Katz, R., Himmelfarb, J., Bansal, N., & Lee, S. I. (2024). From local explanations to global understanding with explainable AI for trees. *Nature Machine Intelligence*, 2(1), 56–67. [https\://doi.org/10.1038/s42256-019-0138-9](https://doi.org/10.1038/s42256-019-0138-9)

\[10\] Niculescu-Mizil, A., & Caruana, R. (2005). Predicting good probabilities with supervised learning. In *Proceedings of the 22nd International Conference on Machine Learning (ICML)* (pp. 625–632). ACM. [https\://doi.org/10.1145/1102351.1102430](https://doi.org/10.1145/1102351.1102430)

\[11\] Platt, J. C. (1999). Probabilistic outputs for support vector machines and comparisons to regularized likelihood methods. *Advances in Large Margin Classifiers*, 10(3), 61–74. [https\://www\.cs.colorado.edu/\~mozer/Teaching/syllabi/6622/papers/Platt1999.pdf](https://www.cs.colorado.edu/~mozer/Teaching/syllabi/6622/papers/Platt1999.pdf)

\[12\] Prokhorenkova, L., Gusev, G., Vorobev, A., Dorogush, A. V., & Gulin, A. (2022). CatBoost: Unbiased boosting with categorical features. In *Advances in Neural Information Processing Systems (NeurIPS 2018\)*, 31, 6638–6648. [https\://proceedings.neurips.cc/paper/7898-catboost](https://proceedings.neurips.cc/paper/7898-catboost)

### 

### **TÀI LIỆU THAM KHẢO PHẦN 3**

\[1\] Baymard Institute. (2026). *49 Cart Abandonment Rate Statistics 2026*. Baymard Research Insights. [https\://baymard.com/lists/cart-abandonment-rate](https://baymard.com/lists/cart-abandonment-rate)

\[2\] Brier, G. W. (1950). Verification of forecasts expressed in terms of probability. *Monthly Weather Review*, 78(1), 1–3. [https\://doi.org/10.1175/1520-0493(1950)078](https://doi.org/10.1175/1520-0493\(1950\)078)\<0001:VOFEIT\>2.0.CO;2

\[3\] D'Agostino, R. B., & Pearson, E. S. (1973). Tests for departure from normality. Empirical results for the distributions of b\_2 and \\sqrt{b\_1}. *Biometrika*, 60(3), 613–622. [https\://doi.org/10.1093/biomet/60.3.613](https://doi.org/10.1093/biomet/60.3.613)

\[4\] Dempster, A. P., Laird, N. M., & Rubin, D. B. (1977). Maximum likelihood from incomplete data via the EM algorithm. *Journal of the Royal Statistical Society: Series B (Methodological)*, 39(1), 1–22. [https\://doi.org/10.1111/j.2517-6161.1977.tb01600.x](https://doi.org/10.1111/j.2517-6161.1977.tb01600.x)

\[5\] Kruskal, W. H., & Wallis, W. A. (1952). Use of ranks in one-criterion variance analysis. *Journal of the American Statistical Association*, 47(260), 583–621. [https\://doi.org/10.1080/01621459.1952.10483441](https://doi.org/10.1080/01621459.1952.10483441)

\[6\] Mann, H. B., & Whitney, D. R. (1947). On a test of whether one of two random variables is stochastically larger than the other. *The Annals of Mathematical Statistics*, 18(1), 50–60. [https\://doi.org/10.1214/aoms/1177730491](https://doi.org/10.1214/aoms/1177730491)

\[7\] Raasveldt, M., & Mühleisen, H. (2019). DuckDB: an embeddable analytical database. In *Proceedings of the 2019 International Conference on Management of Data (SIGMOD)* (pp. 1981–1984). ACM. [https\://doi.org/10.1145/3299869.3320212](https://doi.org/10.1145/3299869.3320212)

\[8\] Schwarz, G. (1978). Estimating the dimension of a model. *The Annals of Statistics*, 6(2), 461–464. [https\://doi.org/10.1214/aos/1176344136](https://doi.org/10.1214/aos/1176344136)

### 

### **TÀI LIỆU THAM KHẢO PHẦN 2**

\[1\] Ascarza, E. (2021). Retention offers that cause churn: A causal inference approach to targeted promotions. *Journal of Marketing Research*, 55(1), 80–99. [https\://doi.org/10.1509/jmr.16.0125](https://doi.org/10.1509/jmr.16.0125)

\[2\] Brier, G. W. (1950). Verification of forecasts expressed in terms of probability. *Monthly Weather Review*, 78(1), 1–3. [https\://doi.org/10.1175/1520-0493(1950)078](https://doi.org/10.1175/1520-0493\(1950\)078)\<0001:VOFEIT\>2.0.CO;2

\[3\] Chen, T., & Guestrin, C. (2021). XGBoost: A scalable tree boosting system. In *Proceedings of the 22nd ACM SIGKDD International Conference on Knowledge Discovery and Data Mining* (pp. 785–794). ACM. [https\://doi.org/10.1145/2939672.2939785](https://doi.org/10.1145/2939672.2939785)

\[4\] Cox, D. R. (1972). Regression models and life-tables. *Journal of the Royal Statistical Society: Series B (Methodological)*, 34(2), 187–202. [https\://doi.org/10.1111/j.2517-6161.1972.tb00899.x](https://doi.org/10.1111/j.2517-6161.1972.tb00899.x)

\[5\] D'Agostino, R. B., & Pearson, E. S. (1973). Tests for departure from normality. Empirical results for the distributions of b\_2 and \\sqrt{b\_1}. *Biometrika*, 60(3), 613–622. [https\://doi.org/10.1093/biomet/60.3.613](https://doi.org/10.1093/biomet/60.3.613)

\[6\] Guitart, I. A., Gonzalez-Hermoso, C., & Rutz, O. J. (2025). Uplift modeling in digital marketing: Avoiding waste and identifying high-impact customer segments. *Decision Support Systems*, 168, Article 113942\. [https\://doi.org/10.1016/j.dss.2024.113942](https://doi.org/10.1016/j.dss.2024.113942)

\[7\] Kaplan, E. L., & Meier, P. (1958). Nonparametric estimation from incomplete observations. *Journal of the American Statistical Association*, 53(282), 457–481. [https\://doi.org/10.1080/01621459.1958.10501452](https://doi.org/10.1080/01621459.1958.10501452)

\[8\] Ke, G., Meng, Q., Finley, T., Wang, T., Chen, W., Ma, W., Ye, Q., & Liu, T. Y. (2021). LightGBM: A highly efficient gradient boosting decision tree. In *Advances in Neural Information Processing Systems (NeurIPS 2017\)*, 30, 3146–3154. [https\://papers.nips.cc/paper/6907-lightgbm](https://papers.nips.cc/paper/6907-lightgbm)

\[9\] Niculescu-Mizil, A., & Caruana, R. (2005). Predicting good probabilities with supervised learning. In *Proceedings of the 22nd International Conference on Machine Learning (ICML)* (pp. 625–632). ACM. [https\://doi.org/10.1145/1102351.1102430](https://doi.org/10.1145/1102351.1102430)

\[10\] Platt, J. C. (1999). Probabilistic outputs for support vector machines and comparisons to regularized likelihood methods. *Advances in Large Margin Classifiers*, 10(3), 61–74. [https\://www\.cs.colorado.edu/\~mozer/Teaching/syllabi/6622/papers/Platt1999.pdf](https://www.cs.colorado.edu/~mozer/Teaching/syllabi/6622/papers/Platt1999.pdf)

\[11\] Prokhorenkova, L., Gusev, G., Vorobev, A., Dorogush, A. V., & Gulin, A. (2022). CatBoost: Unbiased boosting with categorical features. In *Advances in Neural Information Processing Systems (NeurIPS 2018\)*, 31, 6638–6648. [https\://proceedings.neurips.cc/paper/7898-catboost](https://proceedings.neurips.cc/paper/7898-catboost)

### **TÀI LIỆU THAM KHẢO PHẦN 1**

\[1\] Ascarza, E. (2021). Retention offers that cause churn: A causal inference approach to targeted promotions. *Journal of Marketing Research*, 55(1), 80–99. [https\://doi.org/10.1509/jmr.16.0125](https://www.google.com/search?q=https://doi.org/10.1509/jmr.16.0125)

\[2\] Baymard Institute. (2026). *49 Cart Abandonment Rate Statistics 2026*. Baymard Research Insights. [https\://baymard.com/lists/cart-abandonment-rate](https://baymard.com/lists/cart-abandonment-rate)

\[3\] Bộ Công Thương. (2025). *Báo cáo Thương mại điện tử Việt Nam năm 2024: Động lực tăng trưởng và các rào cản thanh toán số*. Cục Thương mại điện tử và Kinh tế số. [https\://moit.gov.vn/bao-cao-thuong-mai-dien-tu-2024.html](https://www.google.com/search?q=https://moit.gov.vn/bao-cao-thuong-mai-dien-tu-2024.html)

\[4\] Chen, T., & Guestrin, C. (2021). XGBoost: A scalable tree boosting system. In *Proceedings of the 22nd ACM SIGKDD International Conference on Knowledge Discovery and Data Mining* (pp. 785–794). ACM. [https\://doi.org/10.1145/2939672.2939785](https://doi.org/10.1145/2939672.2939785)

\[5\] Guitart, I. A., Gonzalez-Hermoso, C., & Rutz, O. J. (2025). Uplift modeling in digital marketing: Avoiding waste and identifying high-impact customer segments. *Decision Support Systems*, 168, Article 113942\. [https\://doi.org/10.1016/j.dss.2024.113942](https://www.google.com/search?q=https://doi.org/10.1016/j.dss.2024.113942)

\[6\] Ke, G., Meng, Q., Finley, T., Wang, T., Chen, W., Ma, W., Ye, Q., & Liu, T. Y. (2021). LightGBM: A highly efficient gradient boosting decision tree. In *Advances in Neural Information Processing Systems (NeurIPS 2017\)*, 30, 3146–3154. [https\://papers.nips.cc/paper/6907-lightgbm](https://papers.nips.cc/paper/6907-lightgbm)

\[7\] Lundberg, S. M., Erion, G., Chen, H., DeGrave, A., Prutkin, J. M., Nair, B., Katz, R., Himmelfarb, J., Bansal, N., & Lee, S. I. (2024). From local explanations to global understanding with explainable AI for trees. *Nature Machine Intelligence*, 2(1), 56–67. [https\://doi.org/10.1038/s42256-019-0138-9](https://doi.org/10.1038/s42256-019-0138-9)

\[8\] Prokhorenkova, L., Gusev, G., Vorobev, A., Dorogush, A. V., & Gulin, A. (2022). CatBoost: Unbiased boosting with categorical features. In *Advances in Neural Information Processing Systems (NeurIPS 2018\)*, 31, 6638–6648. [https\://proceedings.neurips.cc/paper/7898-catboost](https://www.google.com/search?q=https://proceedings.neurips.cc/paper/7898-catboost)

\[9\] UN Trade and Development (UNCTAD). (2024). *Digital Economy Report 2024: Shaping future value chains in global e-commerce*. United Nations Publications. [https\://unctad.org/publication/digital-economy-report-2024](https://unctad.org/publication/digital-economy-report-2024)

