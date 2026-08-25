# Optical Character Recognition (OCR) Fundamentals

## Before You Start — Try These First

- If you scan a handwritten medical form into a PDF, why can't you immediately copy-paste text from it into a spreadsheet?
- A logistics company receives invoices in 47 different fonts and layouts — why would simple pattern matching OCR fail here?
- When an OCR system returns a confidence score with extracted text, what decision does that score help you make?

## Learning Objectives

- Explain how OCR converts images containing text into machine-readable data and why this matters for business workflows
- Distinguish between pattern matching and feature extraction as text recognition approaches
- Differentiate OCR, ICR, and IWR based on what unit of text they process and how they handle variation
- Identify which OCR approach (simple vs intelligent) suits a given document scenario based on font predictability and layout complexity

## Discrimination

- You're processing typewritten invoices from 1985, all in Courier font, versus modern invoices in hundreds of different fonts and layouts. Which requires pattern matching and which requires feature extraction, and why? >> 1985 invoices can use pattern matching because they match a single stored font template. Modern varied invoices need feature extraction because it identifies character components (curves, intersections) that work across any font, not just exact matches. *(key difference: Pattern matching requires the input to match stored font templates exactly; feature extraction identifies universal character features that generalize across fonts.)*
- You're building a system to read both printed forms and handwritten prescriptions. Why does the handwriting requirement force you from simple OCR to ICR? >> Simple OCR stores fixed font templates that can't capture unlimited handwriting styles. ICR uses neural networks that learn character features the way humans do, handling variation in handwriting that template matching cannot. *(key difference: Simple OCR matches against stored templates; ICR uses machine learning to recognize features across unlimited styles including handwriting.)*
- You need to extract text from both scanned legal contracts and product photos from social media. Why does the second task push beyond standard OCR into computer vision? >> Legal contracts are document images where text is the primary content. Product photos have text (logos, labels) as one element in complex scenes requiring object detection, brand recognition, and scene understanding — capabilities that belong to computer vision with embedded OCR, not standalone OCR. *(key difference: Document OCR assumes text is the primary content; computer vision embeds OCR as one component in scene analysis with multiple objects and contexts.)*
- An OCR system can process characters one at a time (ICR) or entire words at once (IWR). When would processing whole words matter more than individual characters? >> IWR matters when context and word shape aid recognition — like reading degraded or stylized text where individual characters are ambiguous but the whole word shape is recognizable. ICR is more universal but IWR can be faster and more accurate for complete words in difficult images. *(key difference: ICR processes one character at a time; IWR processes whole-word images without character-level preprocessing.)*

## Scenario Cards

- A hospital receives thousands of handwritten patient intake forms daily. Staff spend hours typing information into the system. You propose an OCR solution. What type of OCR do you need and what preprocessing challenges should you anticipate? >> You need ICR (Intelligent Character Recognition) because handwriting varies too much for simple pattern matching. Preprocessing challenges include deskewing forms filled at angles, despeckling pen marks and paper texture, and handling crossed-out corrections or notes in margins.
- You're building a mobile app where users photograph receipts for expense reports. The photos are taken at various angles, in different lighting, with wrinkled paper. What makes this harder than scanning a flat document, and what technology do you need? >> Variable angles require deskewing, lighting variations create inconsistent dark/light classification, and wrinkles distort character shapes. You need ICR with robust preprocessing and ideally a system trained on real-world photo conditions, not just clean scans. Real-time image capture also demands fast processing.
- A logistics company processes invoices from hundreds of vendors in different formats, fonts, and languages. Some are typed, some handwritten, some are tables. Why is simple OCR inadequate and what additional capabilities do you need? >> Simple OCR only handles known fonts via pattern matching and cannot handle format variation, handwriting, or complex layouts like tables. You need ICR for handwriting and font variation, table extraction capabilities to preserve structure, multi-language support, and likely machine learning to handle layout diversity without manual template creation.
- A company scans 50-year-old typewritten contracts for a legal archive. All documents used IBM Selectric typewriters with identical fonts, but the paper has yellowed and some pages are slightly tilted. What OCR approach is sufficient and what preprocessing matters most? >> Pattern matching OCR is sufficient because the font is uniform and can be stored as templates. Deskewing is the critical preprocessing step to fix tilted scans so characters align with stored templates. Despeckling may help with paper discoloration.

## Concept Cards

- Why does converting paper documents to searchable text archives matter for business analytics software? >> Text in image files is hidden from software. Converting it to text data allows automated analysis, search, workflow integration, and knowledge processing that images cannot support.
- You scan a 1960s typewritten memo. The OCR system deskews it, despeckles it, and removes border lines. What stage of OCR is this? >> Preprocessing. This is the cleanup stage after image acquisition and before text recognition, preparing the image for accurate reading.
- A bank wants to automate processing of deposit checks. Why is OCR essential for this workflow? >> Checks arrive as images (scanned or photographed). OCR extracts account numbers, amounts, and payee information into data that banking software can verify and process automatically, eliminating manual entry.

## Cloze

- If you scan a form or receipt, your computer saves it as an image file where you cannot use a text editor to edit, search, or count the words — but OCR {{c1::converts the image into a text document with contents stored as text data}}.
- Feature extraction breaks down glyphs into features such as {{c1::lines, closed loops, line direction, and line intersections}}, then uses these features to find the best match among stored glyphs.
- Modern OCR systems use intelligent character recognition technology to read text the same way humans do, training machines through {{c1::neural networks that analyze images over many levels}}.

## Recall Cards

- What does OCR stand for and what does it convert? >> Optical Character Recognition. It converts images of text into machine-readable text data.
- Name the two main OCR text recognition algorithms. >> Pattern matching and feature extraction.

## Multiple Choice

- An OCR system completes preprocessing and begins text recognition. It isolates the letter 'B' and compares it pixel-by-pixel against stored images of every letter in Arial 12pt font. What algorithm is this?
    - A. Pattern matching
    - B. Intelligent character recognition
    - C. Optical mark recognition
    - D. Feature extraction
    - >> A. Pattern matching
        - Pattern matching compares the input character image directly against stored templates (glyphs) of known fonts. It requires the input to match the stored font and scale. Feature extraction would identify components like lines and loops rather than compare whole character images, and ICR would use neural networks rather than direct template comparison.
- A finance company wants to automatically verify loan documents by reading customer signatures and checking account numbers. The account numbers are printed in standard fonts but signatures are handwritten. What does this require?
    - A. Pattern matching for signatures, feature extraction for account numbers
    - B. ICR for signatures, simple OCR acceptable for printed account numbers
    - C. Simple OCR for everything since both are on paper
    - D. Only optical mark recognition since signatures are marks not text
    - >> B. ICR for signatures, simple OCR acceptable for printed account numbers
        - Handwritten signatures require ICR because handwriting styles are unlimited and need machine learning to recognize. Printed account numbers in standard fonts can work with simple pattern-matching OCR. Optical mark recognition is for logos and symbols, not text. Signatures involve character recognition (letters), not just mark detection.
- After OCR processes an invoice, it outputs both the original scanned image and a text file with all extracted content. What stage created this combined output?
    - A. Text recognition
    - B. Image acquisition
    - C. Postprocessing
    - D. Preprocessing
    - >> C. Postprocessing
        - Postprocessing is the final stage that converts extracted text data into machine-readable formats and can create annotated PDFs combining original and extracted versions. Image acquisition captures the initial scan, preprocessing cleans it, and text recognition extracts the content — but only postprocessing assembles the final output format.
- A system needs to detect company logos in social media posts to track brand mentions. Is this standard document OCR?
    - A. No, this is optical mark recognition, a specialized OCR type
    - B. No, this requires computer vision with embedded OCR capabilities
    - C. Yes, logos are text that OCR reads
    - D. Yes, but only if the logos include readable words
    - >> A. No, this is optical mark recognition, a specialized OCR type
        - Optical mark recognition is specifically for identifying logos, watermarks, and symbols within documents. While related to OCR, detecting logos in social media posts is explicitly called out as optical mark recognition in the source material.

## Teach Back

- Explain to a non-technical manager why converting your company's paper invoice archive to PDFs isn't enough to make them searchable, and what OCR adds.
  - Scanning creates image files where text is pixels, not data
  - Software cannot search, edit, or analyze text trapped in images
  - OCR converts those pixels into actual text data that systems can process
  - This enables search across thousands of documents, automated data extraction, and workflow integration

## Apply This Today

- [ ] Find a printed receipt or form in your home. Photograph it with your phone, then use a free OCR tool (many phone note apps include OCR, or try a web-based tool) to extract the text. Compare what it gets right versus wrong. What preprocessing issues (tilt, lighting, wrinkles) caused the errors? This takes about 15 minutes and makes preprocessing tangible.
- [ ] Identify one repetitive task at work where someone manually types information from images, PDFs, or scanned documents into a system. Write three sentences describing: (1) what document type it is, (2) whether the text is printed or handwritten, and (3) whether simple OCR or ICR would be needed and why. This forces you to apply the discrimination between OCR types to a real scenario.