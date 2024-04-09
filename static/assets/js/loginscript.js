// Function to populate images for col1

function populateImagesForCol1() {
    const col1 = document.getElementById('col1');
    const imageUrls = [
        "firstframe.jpg",
        "secondframe.jpg",
        "thirdframe.jpg",
        "fourthframe.jpg",
        "fifthframe.jpg",
        "sixthframe.jpg",
        "sixthframe.jpg",
        "sixthframe.jpg",

    ];

    // Loop through image URLs and create image elements
    imageUrls.forEach((url, index) => {
        const img = document.createElement('img');
        img.src = url;
        img.alt = `Image ${index + 1}`;
        img.classList.add('rounded-image'); // Add a class for styling
        col1.appendChild(img);
    });
}

// Function to populate images for col2
function populateImagesForCol2() {
    const col2 = document.getElementById('col2');
    const imageUrls = [
        "firstframe.jpg",
        "secondframe.jpg",
        "thirdframe.jpg",
        "fourthframe.jpg",
        "fifthframe.jpg",
        "sixthframe.jpg",
        "sixthframe.jpg",
        "sixthframe.jpg",
        "sixthframe.jpg",
        "sixthframe.jpg",
    ];

    // Loop through image URLs and create image elements
    imageUrls.forEach((url, index) => {
        const img = document.createElement('img');
        img.src = url;
        img.alt = `Image ${index + 1}`;
        img.classList.add('rounded-image'); // Add a class for styling
        col2.appendChild(img);
    });
}

// Repeat the pattern for col3, col4, col5, and col6
// Function to populate images for col3
function populateImagesForCol3() {
    const col3 = document.getElementById('col3');
    const imageUrls = [
        "seven.jpg",
        "eightframe.jpg",
        "nineframe.jpg",
        "tenframe.jpg",
        "elevenframe.jpg",
        "twelveframe.jpg",
        "twelveframe.jpg",
        "twelveframe.jpg",
        "twelveframe.jpg",
    ];

    // Loop through image URLs and create image elements
    imageUrls.forEach((url, index) => {
        const img = document.createElement('img');
        img.src = url;
        img.alt = `Image ${index + 1}`;
        img.classList.add('rounded-image'); // Add a class for styling
        col3.appendChild(img);
    });
}

// Function to populate images for col4
function populateImagesForCol4() {
    const col4 = document.getElementById('col4');
    const imageUrls = [
        "firstframe.jpg",
        "secondframe.jpg",
        "thirdframe.jpg",
        "fourthframe.jpg",
        "fifthframe.jpg",
        "sixthframe.jpg",
        "sixthframe.jpg",
        "sixthframe.jpg",
        "sixthframe.jpg",
    ];

    // Loop through image URLs and create image elements
    imageUrls.forEach((url, index) => {
        const img = document.createElement('img');
        img.src = url;
        img.alt = `Image ${index + 1}`;
        img.classList.add('rounded-image'); // Add a class for styling
        col4.appendChild(img);
    });
}

// Function to populate images for col5
function populateImagesForCol5() {
    const col5 = document.getElementById('col5');
    const imageUrls = [
        "elevenframe.jpg",
        "twelveframe.jpg",
        "thirteenframe.jpg",
        "fourteenframe.jpg",
        "fifteenframe.jpg",
        'sixteenframe.jpg'
        // Add more image URLs as needed
    ];

    // Loop through image URLs and create image elements
    imageUrls.forEach((url, index) => {
        const img = document.createElement('img');
        img.src = url;
        img.alt = `Image ${index + 1}`;
        img.classList.add('rounded-image'); // Add a class for styling
        col5.appendChild(img);
    });
}

// Function to populate images for col6
function populateImagesForCol6() {
    const col6 = document.getElementById('col6');
    const imageUrls = [
        "elevenframe.jpg",
        "twelveframe.jpg",
        "thirteenframe.jpg",
        "fourteenframe.jpg",
        "fifteenframe.jpg",
        'sixteenframe.jpg'
        // Add more image URLs as needed
    ];

    // Loop through image URLs and create image elements
    imageUrls.forEach((url, index) => {
        const img = document.createElement('img');
        img.src = url;
        img.alt = `Image ${index + 1}`;
        img.classList.add('rounded-image'); // Add a class for styling
        col6.appendChild(img);
    });
}

// Call functions to populate images for each column
populateImagesForCol1();
populateImagesForCol2();
populateImagesForCol3();
populateImagesForCol4();
populateImagesForCol5();
populateImagesForCol6();

// Auto-scrolling function
function autoScroll() {
    const scrollSpeed = 1; // Adjust scrolling speed as needed

    // Scroll up column 1
    const column1 = document.getElementById('col1');
    if (column1.scrollTop <= 0) {
        column1.scrollTop = column1.scrollHeight; // Reset to bottom if it reaches the top
    } else {
        column1.scrollTop -= scrollSpeed;
    }

    // Scroll down column 2
    const column2 = document.getElementById('col2');
    column2.scrollTop += scrollSpeed;

    // Scroll up column 3
    const column3 = document.getElementById('col3');
    if (column3.scrollTop <= 0) {
        column3.scrollTop = column3.scrollHeight; // Reset to bottom if it reaches the top
    } else {
        column3.scrollTop -= scrollSpeed;
    }

    // Scroll down column 4
    const column4 = document.getElementById('col4');
    column4.scrollTop += scrollSpeed;

    // Scroll up column 5
    const column5 = document.getElementById('col5');
    if (column5.scrollTop <= 0) {
        column5.scrollTop = column5.scrollHeight; // Reset to bottom if it reaches the top
    } else {
        column5.scrollTop -= scrollSpeed;
    }

    // Scroll down column 6
    const column6 = document.getElementById('col6');
    column6.scrollTop += scrollSpeed;
}

// Call auto-scroll function every 30 milliseconds
setInterval(autoScroll, 30);
// Function to hide columns 5 and 6 if window width is 1000px or less
function hideColumnsForSmallScreens() {
    const windowWidth = window.innerWidth; // Get the width of the window

    // Check if the window width is less than or equal to 400px
    if (windowWidth <= 400) {
        // Hide columns 3, 4, 5, and 6
        document.getElementById('col3').style.display = 'none';
        document.getElementById('col4').style.display = 'none';
        document.getElementById('col5').style.display = 'none';
        document.getElementById('col6').style.display = 'none';
    } else if (windowWidth <= 650) { // Check if the window width is less than or equal to 650px
        // Hide columns 4, 5, and 6
        document.getElementById('col4').style.display = 'none';
        document.getElementById('col5').style.display = 'none';
        document.getElementById('col6').style.display = 'none';
    } 
     else if (windowWidth <= 850) { // Check if the window width is less than or equal to 650px
        // Hide columns 4, 5, and 6
        document.getElementById('col5').style.display = 'none';
        document.getElementById('col6').style.display = 'none';
    }
    else if (windowWidth <= 1200) { // Check if the window width is less than or equal to 650px
        // Hide columns 4, 5, and 6
        document.getElementById('col6').style.display = 'none';
    }  else {
        // Ensure all columns are visible
        document.getElementById('col3').style.display = 'block';
        document.getElementById('col4').style.display = 'block';
        document.getElementById('col5').style.display = 'block';
        document.getElementById('col6').style.display = 'block';
    }
}

// Call the function initially to set the visibility of columns based on screen size
hideColumnsForSmallScreens();

// Listen for window resize events to adjust column visibility
window.addEventListener('resize', hideColumnsForSmallScreens);
