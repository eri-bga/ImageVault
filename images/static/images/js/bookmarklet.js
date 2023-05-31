const siteUrl = '//127.0.0.1:8000/';
const styleUrl = siteUrl + 'static/images/css/bookmarklet.css';
const minWidth = 250;
const minHeight = 250;

// load css
let head = document.getElementsByTagName('head')[0];
let link = document.createElement('link');
link.rel = 'stylesheet';
link.type = 'text/css';
link.href = styleUrl + '?=r' + Math.floor(Math.random() * 9999999999999999);
head.appendChild(link);

// Load html
let body = document.getElementsByTagName('body')[0];
let boxHtml = `
    <div id="bookmarklet">
        <a href="#" id="close">&times;</a>
        <h1>Select an image to bookmark:</h1>
        <div class="images"></div>
    </div>
`;
body.innerHTML += boxHtml;


function bookmarkLetLaunch() {
    let bookmarkLet = document.getElementById('bookmarklet');
    let imagesFound = bookmarkLet.querySelector('.images');

    // clear images found
    imagesFound.innerHTML = '';
    // display bookmarklet
    bookmarkLet.style.display = 'block';

    // Close event
    bookmarkLet.querySelector('#close').addEventListener('click', function(){
        bookmarkLet.style.display = 'none';
    });

    // Find images in the Dom with the minimum dimensions
    let images = document.querySelectorAll('img[src$=".jpg"], img[src$=".jpeg"], img[src$=".png"]');
    if (!images) {
        imagesFound.innerHTML = 'No images found';
    }
    images.forEach(image => {
        if(image.naturalWidth >= minWidth && image.naturalHeight >= minHeight) {
            let imageFound = document.createElement("img");
            imageFound.src = image.src;
            imagesFound.append(imageFound);
        }
    })

    // Select image event
    imagesFound.querySelectorAll("img").forEach(image => {
        image.addEventListener("click", function(event) {
            let imageSelected = event.target;
            bookmarkLet.style.display = "none";
            window.open(siteUrl + 'images/create/?url='
                        + encodeURIComponent(imageSelected.src)
                        + '&title=' 
                        + encodeURIComponent(document.title),
                        '_blank');
        })
    })
}

// Launch bookmarklet
bookmarkLetLaunch();