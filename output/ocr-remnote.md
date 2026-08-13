# What is OCR (Optical Character Recognition)?

## Learning Objectives

- Define Optical Character Recognition (OCR) and explain its core function
- Explain why OCR is important for modern business workflows and document processing
- Describe how OCR technology works, including preprocessing, recognition algorithms, and postprocessing
- Identify different types of OCR technologies and their specific applications
- Analyze real-world use cases of OCR across banking, healthcare, and logistics industries

## Recall Cards

- What does OCR stand for and what is its primary function? >> OCR stands for Optical Character Recognition. Its primary function is to convert an image of text into a machine-readable text format that can be edited, searched, and processed by software.
- Name the two main OCR algorithms used for text recognition. >> The two main OCR algorithms are pattern matching and feature extraction.
- What are the three main steps in how OCR works? >> The three main steps are: image acquisition (scanning and converting to binary data), preprocessing (cleaning and preparing the image), and text recognition (analyzing and converting to machine-readable text).
- What is a glyph in OCR terminology? >> A glyph is an isolated character image that OCR software analyzes and compares against stored character templates during the recognition process.
- Name three preprocessing techniques used in OCR. >> Three preprocessing techniques are: deskewing (correcting alignment), despeckling (removing digital noise), and cleaning up boxes and lines in the image.
- When was one of the first known OCR developments created and by whom? >> One of the first known OCR developments was Emanuel Goldberg's machine in the 1920s, which could read characters and convert them to telegraph code.
- What were OCR-A and OCR-B, and when were they introduced? >> OCR-A and OCR-B were fonts designed in the 1960s to be easily read by both humans and machines, allowing OCR to become more consistent across finance and government applications.
- Name two AWS services that provide OCR capabilities. >> Amazon Textract and Amazon Rekognition are two AWS services that provide OCR capabilities.

## Concept Cards

- Why is OCR important for businesses moving toward paperless document management? >> OCR is important because simply scanning paper documents creates image files with text hidden inside them, which cannot be processed by word processing software. OCR converts these images into analyzable text data, enabling businesses to conduct analytics, automate processes, streamline operations, and improve productivity without manual data entry.
- How does pattern matching differ from feature extraction in OCR? >> Pattern matching compares entire character images against stored templates and requires close font and scale similarity, limiting its flexibility. Feature extraction breaks characters into component features like lines and loops, then finds the best match based on these features, allowing it to recognize a wider variety of fonts and styles.
- Why can't you simply use a text editor on a scanned document without OCR? >> When you scan a document, the computer saves it as an image file. Text in images is essentially picture data, not actual text characters. A text editor cannot recognize, edit, search, or count words in image data—it needs actual text characters, which is what OCR provides by analyzing and converting the image.
- How does Intelligent Character Recognition (ICR) work differently than simple OCR? >> ICR uses neural networks and machine learning to analyze text at multiple levels, similar to how humans read. It processes images repeatedly, looking for different attributes like curves, lines, and intersections, then combines results from all analysis levels. This allows ICR to handle diverse fonts, handwriting, and varying image quality that simple pattern-matching OCR cannot.
- What role does preprocessing play in OCR accuracy? >> Preprocessing cleans and optimizes scanned images before text recognition, removing errors that could cause misreading. By correcting alignment through deskewing, removing noise through despeckling, smoothing edges, and cleaning up boxes and lines, preprocessing ensures the recognition algorithms receive the clearest possible input, significantly improving accuracy.
- How does OCR enable artificial intelligence solutions beyond simple text extraction? >> OCR provides the text recognition foundation that other AI systems build upon. For example, it reads number plates in self-driving cars, detects brand logos in social media posts, and identifies product packaging in advertising. By converting visual text into data, OCR enables AI systems to make marketing and operational decisions, reduce expenses, and improve customer experiences.

## Scenario Cards

- A logistics company receives thousands of invoices daily in different formats from various suppliers. Manual data entry is slow and error-prone. How would OCR technology solve this problem? >> OCR would scan and convert the invoice images into machine-readable text automatically. The system would extract key information like invoice numbers, amounts, dates, and line items regardless of different layouts. This eliminates manual data entry, reduces errors, speeds up processing, and allows the data to integrate directly into accounting systems for automated processing and analytics.
- A hospital needs to digitize decades of handwritten patient records stored in filing cabinets to make them searchable. What type of OCR technology would be most appropriate and why? >> Intelligent Character Recognition (ICR) would be most appropriate because handwritten records vary greatly in style and quality. ICR uses neural networks to analyze text at multiple levels like humans do, allowing it to interpret diverse handwriting styles. Simple pattern-matching OCR would fail because handwriting doesn't match stored font templates. ICR can also handle poor-quality scans from aging documents.
- A bank wants to enable customers to deposit checks by taking photos with their mobile phones. What OCR challenges does this present and how might modern OCR address them? >> Mobile check photos present challenges like varying lighting, angles, image quality, and potential skewing. Modern OCR addresses these through preprocessing (deskewing to fix alignment, despeckling to remove noise, edge smoothing) and ICR technology that can interpret text despite variations. The system would extract account numbers, amounts, and signatures from the check image in real-time, verify the data, and process the deposit automatically.
- A research institution has thousands of historical documents they want to make searchable for specific names, dates, and topics. How does OCR enable this, and what additional processing might be needed? >> OCR converts the document images into machine-readable text that can be indexed and searched. After extraction, the text would be processed through natural language processing (NLP) for entity recognition to identify names, dates, and topics. The extracted text could be stored in a searchable database where users can quickly find relevant documents without manually sorting through files, creating a fully searchable knowledge archive.
- A company receives forms filled out by hand from customers. They need to extract specific field values and verify the information automatically. What OCR capabilities would this require? >> This requires OCR with form field identification and structured data extraction capabilities. The system would need ICR to read handwriting, field detection to identify where specific information appears regardless of slight form variations, and data extraction to pull values in a structured format for database integration. Modern OCR systems like Amazon Textract can identify fields and extract structured information for automated verification, review, and analysis without manual data entry.

## Multiple Choice

- What is the primary difference between a scanned document saved as an image and the same document processed with OCR? >>A)
  - The OCR output contains machine-readable text data while the scanned image does not
  - The scanned image has better resolution than OCR output
  - The scanned image can be edited in a text editor but OCR output cannot
  - The scanned image takes up less storage space than OCR output
    - Explanation: When you scan a document, it's saved as an image file where the text is part of the picture data and cannot be edited, searched, or processed as text. OCR analyzes the image and converts it into actual machine-readable text data that word processing software can work with. This is the fundamental purpose and value of OCR technology.
- In the image acquisition phase of OCR, how does the software classify the scanned image? >>A)
  - It classifies light areas as background and dark areas as text
  - It separates text from images and graphics
  - It identifies the font type and size of each character
  - It converts color images to grayscale
    - Explanation: During image acquisition, after the scanner converts the document to binary data, the OCR software analyzes the scanned image and performs a basic classification: light areas are identified as background and dark areas as text. This fundamental separation is the first step in preparing the image for the preprocessing and recognition phases.
- Which OCR preprocessing technique corrects alignment issues that may have occurred during scanning? >>A)
  - Deskewing
  - Despeckling
  - Feature extraction
  - Script recognition
    - Explanation: Deskewing is the preprocessing technique that tilts the scanned document slightly to fix alignment issues that occurred during the scan. Despeckling removes digital noise, feature extraction is part of text recognition (not preprocessing), and script recognition identifies languages. Proper alignment through deskewing is essential for accurate character recognition.
- What technological advancement in the 2000s enabled OCR to interpret handwritten text and complex layouts with greater accuracy? >>A)
  - Neural networks and early machine learning
  - The invention of OCR-A and OCR-B fonts
  - Faster scanner hardware
  - Cloud computing services
    - Explanation: According to the source material, in the 2000s, neural networks and early machine learning technology enabled OCR to go beyond fixed fonts and layouts. This allowed modern OCR systems to interpret handwritten text, poor-quality scans, and complex layouts with far greater accuracy than earlier pattern-matching systems could achieve.
- How did BlueVine use OCR technology during the COVID-19 pandemic? >>A)
  - To process and analyze tens of thousands of PPP loan forms per day
  - To verify customer identities through passport scanning
  - To convert medical records into digital format
  - To read check deposits from mobile phones
    - Explanation: BlueVine used Amazon Textract OCR to automatically process and analyze tens of thousands of Paycheck Protection Program (PPP) forms per day during the COVID-19 relief stimulus. This enabled them to help several thousand small businesses access funds quickly, ultimately saving over 400,000 jobs. This demonstrates OCR's capability to handle high-volume, time-critical document processing.
- What advantage does Intelligent Character Recognition (ICR) have over simple pattern-matching OCR? >>A)
  - ICR can handle virtually unlimited font and handwriting styles while pattern matching cannot
  - ICR processes documents faster than pattern matching
  - ICR requires less computational power than pattern matching
  - ICR works better with typed documents than pattern matching
    - Explanation: The source material explains that simple pattern-matching OCR has limitations because there are virtually unlimited font and handwriting styles that cannot all be captured and stored in a database. ICR overcomes this by using neural networks to analyze text like humans do, processing images at multiple levels to recognize diverse fonts and handwriting styles that pattern matching would miss.

## Teach Back

- Explain how OCR technology works from start to finish, as if you were teaching someone who has never heard of it before. Include the three main phases and what happens in each.
  - Image acquisition: scanner reads document and converts to binary data, software classifies light areas as background and dark areas as text
  - Preprocessing: software cleans the image through deskewing (fixing alignment), despeckling (removing noise), smoothing edges, and cleaning up boxes and lines
  - Text recognition: uses pattern matching or feature extraction algorithms to identify characters
  - Postprocessing: converts extracted text into machine-readable documents, sometimes creating annotated PDFs with before and after versions
- Teach someone the difference between pattern matching and feature extraction in OCR. When would each approach work best?
  - Pattern matching: isolates character images (glyphs) and compares them to stored templates in database
  - Pattern matching requires similar font and scale to stored glyphs, limiting flexibility
  - Pattern matching works well for scanned documents typed in known fonts
  - Feature extraction: breaks characters into component features like lines, loops, direction, and intersections
  - Feature extraction finds best match based on features rather than whole character shape
  - Feature extraction handles more variation in fonts and styles than pattern matching
- Explain to a business owner why simply scanning their paper documents isn't enough, and how OCR solves the problem they might not know they have.
  - Scanned documents are saved as image files where text is hidden picture data
  - Text in images cannot be edited, searched, or counted by word processing software
  - Manual processing of scanned documents is time-consuming and error-prone
  - OCR converts image text into actual machine-readable text data
  - Machine-readable text enables analytics, automation, searching, and integration with business software
  - OCR streamlines operations, improves productivity, and enables digital transformation
  - Examples: searchable archives, automated form processing, integration with accounting systems
- Describe how Intelligent Character Recognition (ICR) represents an evolution from simple OCR. What makes it 'intelligent'?
  - Simple OCR uses pattern matching against stored font templates, which is limited
  - ICR uses neural networks and machine learning to read like humans do
  - ICR analyzes images at multiple levels repeatedly, not just once
  - ICR examines different attributes: curves, lines, intersections, loops
  - ICR combines results from all analysis levels to determine final result
  - ICR can handle diverse fonts, handwriting styles, and varying image quality
  - ICR typically processes one character at a time but delivers results in seconds
  - ICR represents the modern standard for OCR technology
- Walk through a real-world example of how OCR benefits one specific industry. Choose banking, healthcare, or logistics and explain the before-and-after transformation.
  - Example industry choice and its document processing challenges
  - Specific documents that industry handles (checks, patient records, invoices, etc.)
  - Problems with manual processing: time, errors, fraud risk, or storage issues
  - How OCR automates the extraction and verification process
  - Specific benefits achieved: speed, accuracy, security, or cost reduction
  - Real example if using one from source: BlueVine PPP loans, nib Group claims, or Foresight Group invoices
  - Measurable outcomes: volume processed, time saved, jobs saved, or efficiency gained