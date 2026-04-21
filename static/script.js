const labels = ["Genre:"];
let currentQuestion = 0;
let responses = [];

const genreDropdown = document.getElementById('genres');
const submitBtn = document.getElementById('submitBtn');
const responseList = document.getElementById('responseList');

function displayResponse(label, answer) {
    const responseItem = document.createElement('div');
    responseItem.className = 'response-item';
    responseItem.innerHTML = `<strong>${label}</strong> <span>${answer}</span>`;
    responseList.appendChild(responseItem);
}

async function handleSubmit() {
    const selectedGenre = genreDropdown.value;

    // Validation
    if (!selectedGenre || selectedGenre === 'volvo') {
        alert('Please select a valid genre');
        return;
    }

    try {
        // 1. Fetch the JSON file
        const response = await fetch('./top_5_genres.json');
        if (!response.ok) throw new Error('Could not load JSON file');
        const bookData = await response.json();

        // 2. Display the choice in the response list
        displayResponse(labels[currentQuestion], selectedGenre);
        responses.push(selectedGenre);

        // 3. Get the 5 books for that genre
        const books = bookData[selectedGenre];

        if (books) {
            const bookContainer = document.createElement('div');
            bookContainer.className = 'book-results';
            bookContainer.innerHTML = `<h2>Top 5 ${selectedGenre.toUpperCase()} Books</h2>`;
            
            const list = document.createElement('ul');
            list.style.padding = "0";

            books.forEach(book => {
                const li = document.createElement('li');
                li.style.listStyle = "none";
                li.style.padding = "15px";
                li.style.borderBottom = "1px solid #eee";
                li.innerHTML = `
                    <div style="font-weight: bold; font-size: 1.1em;">${book.title}</div>
                    <div style="color: #666;">Rating: ⭐ ${book.rating} (${book.ratings_count} reviews)</div>
                `;
                list.appendChild(li);
            });

            bookContainer.appendChild(list);
            responseList.appendChild(bookContainer);
        } else {
            alert("No books found for this genre in the JSON file.");
        }

        // 4. Hide the input section so the user only sees the results
        document.querySelector('.input-section').style.display = 'none';

    } catch (error) {
        console.error('Error:', error);
        alert('Error: Make sure you are running this through a Local Server (like Live Server in VS Code) to allow file reading.');
    }
}

submitBtn.addEventListener('click', handleSubmit);
