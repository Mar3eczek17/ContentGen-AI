document.getElementById('content-form').addEventListener('submit', function(event) {
    event.preventDefault();
    
    // Get user input for prompt and language
    let prompt = document.getElementById('prompt').value;
    let language = document.getElementById('language').value;

    // Fetch generated content from the Flask backend
    fetch('/generate', {
        method: 'POST',
        headers: {'Content-Type': 'application/x-www-form-urlencoded'},
        body: 'prompt=' + encodeURIComponent(prompt) + '&language=' + encodeURIComponent(language)
    })
    .then(response => response.json())
    .then(data => {
        // Inject the generated HTML content into the DOM
        document.getElementById('generated-content').innerHTML = data.content;
        document.getElementById('download-pdf').style.display = 'inline-block'; // Show download button
    })
    .catch(error => console.error('Error generating content:', error)); // Error handling
});

// PDF Download Button Event
document.getElementById('download-pdf').addEventListener('click', function() {
    let content = document.getElementById('generated-content');

    // Use html2canvas to capture the content as a canvas
    html2canvas(content, { scale: 2, useCORS: true }).then(canvas => {
        console.log('Canvas created:', canvas); // Debugging: Log the canvas
        let imgData = canvas.toDataURL('image/png'); // Get image data from canvas
        console.log('Image Data URL:', imgData); // Debugging: Log the image data URL
        let { jsPDF } = window.jspdf; // Import jsPDF
        let doc = new jsPDF('p', 'mm', 'a4'); // Create a new PDF document

        let imgWidth = 210; // A4 width in mm
        let pageHeight = 297; // A4 height in mm
        let imgHeight = (canvas.height * imgWidth) / canvas.width; // Calculate height for the image
        let heightLeft = imgHeight; // Remaining height to account for

        let position = 0; // Starting position on the PDF page

        // Add image to PDF, accounting for multiple pages if necessary
        while (heightLeft > 0) {
            // Adjust position and add image to PDF
            doc.addImage(imgData, 'PNG', 0, position, imgWidth, imgHeight);
            heightLeft -= pageHeight; // Subtract page height from remaining height
            position -= pageHeight; // Move to the next page
            if (heightLeft > 0) {
                doc.addPage(); // Add a new page if needed
            }
        }

        // Save the PDF with the specified filename
        doc.save('generated-content.pdf');
    }).catch(error => console.error('Error generating PDF:', error)); // Error handling
});
