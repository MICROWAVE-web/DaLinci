$(document).ready(function () {
    let frm = $('#service_form');
    frm.submit(function () {
        $.ajax({
            type: frm.attr('method'),
            url: frm.attr('action'),
            data: frm.serialize(),
            success: function (data) {
                console.log(data);
                let block = $('.curved-div-inner');
                block.slideUp(200);
                block.promise().done(function () {
                    frm.hide();
                    if (data["error"] === "You already have the same link!") {
                        let addr = window.location;
                        block.html(`
                        <div style="color: rgba(0, 0, 0, 0.5); font-weight: 100; font-size: 1rem;">У вас уже имеется <a style="font-weight: bold; color: #667eea;" href="../links/">ссылка</a> на этот ресурс!</div>
                        <br>
                        <button onclick="location.reload(); return false;" class="btn btn-primary" style="background-color: #667eea;
                        border: 1px solid #6079da;
                        font-weight: bold;">Попробовать ещё
                        </button>
                        `);
                        block.slideDown(200, "swing");
                    } else if (data["abbrlink"]) {
                        let right_link = data["abbrlink"]
                        if (is_authenticated === 'True') {
                            block.html(`
                            <div class="text-center" style="font-weight: bold; font-size: 30px; color: #667eea;">
                            <div style="color: rgba(0, 0, 0, 0.5); font-weight: 100; font-size: 20px;">Ваша ссылка</div>` + right_link + `</div>
                            <br>
                            <div style="font-weight: bold; font-size: 30px; color: black;">Ваш QR код</div>
                            <div class="qrcode" id="qr" style="height: auto; width: auto;"></div>
                            <br>
                            <div style="color: rgba(0, 0, 0, 0.5); font-weight: 100; font-size: 20px;">Вы можете посмотреть статистику вашей сcылки в разделе <a href="../links/?index=2"><div class="text-center" style="font-weight: bold; font-size: 30px; color: #667eea;">Cтатистика</div></a></div>
                            <br>
                            <button onclick="location.reload(); return false;" class="btn btn-primary" style="background-color: #667eea;
                            border: 1px solid #6079da;
                            font-weight: bold;">Ещё</button>
                            `);
                            copyToClipboard(right_link)
                            $('#qr').ClassyQR({
                                create: true,
                                text: right_link
                            });
                        } else {
                            block.html(`
                            <div class="text-center" style="font-weight: bold; font-size: 30px; color: #667eea;">
                            <div style="color: rgba(0, 0, 0, 0.5); font-weight: 100; font-size: 20px;">Ваша ссылка - </div>` + right_link + `</div>
                            <br>
                            <button onclick="location.reload(); return false;" class="btn btn-primary" style="background-color: #667eea;
                            border: 1px solid #6079da;
                            font-weight: bold;">Ещё
                            </button>`);
                        }
                        block.slideDown(200, "swing");

                    }
                });

            },
            error: function (data) {
                console.log('error :(');
            }
        });
        return false;
    });
});

function copyToClipboard(text) {
    let area = document.createElement('textarea');

    document.body.appendChild(area);
    area.value = text;
    area.select();
    document.execCommand("copy");
    document.body.removeChild(area);
}