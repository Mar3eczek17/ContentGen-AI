document.getElementById('content-form').addEventListener('submit', function(event) {
    event.preventDefault();
    let prompt = document.getElementById('prompt').value;
    let language = document.getElementById('language').value;
    fetch('/generate', {
        method: 'POST',
        headers: {'Content-Type': 'application/x-www-form-urlencoded'},
        body: 'prompt=' + encodeURIComponent(prompt) + '&language=' + encodeURIComponent(language)
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById('generated-content').innerHTML = data.content; // Inject HTML content
        document.getElementById('download-pdf').style.display = 'inline-block';
    });
});

document.getElementById('download-pdf').addEventListener('click', function() {
    let content = document.getElementById('generated-content');

    html2canvas(content, { scale: 2 }).then(canvas => {
        let imgData = canvas.toDataURL('image/png');
        let { jsPDF } = window.jspdf;
        let doc = new jsPDF('p', 'mm', 'a4');

        let imgWidth = 210; // A4 width in mm
        let pageHeight = 297; // A4 height in mm
        let imgHeight = canvas.height * imgWidth / canvas.width;
        let heightLeft = imgHeight;

        let position = 0;

        while (heightLeft > 0) {
            doc.addImage(imgData, 'PNG', 0, position, imgWidth, imgHeight);
            heightLeft -= pageHeight;
            position -= 297;
            if (heightLeft > 0) {
                doc.addPage();
            }
        }

        doc.save('generated-content.pdf');
    });
});
