const main = document.getElementById("main");
const form = document.getElementById("form");
const search = document.getElementById("searchInput");

const CSV = "moviedata.csv";
const movies=[]
// Initially display all movies
displayAllMovies();

async function displayAllMovies() {
    const response = await fetch(CSV);
    const data = await response.text();
    const movies = processData(data);
    showMovies(movies);
}

function processData(data) {
    const rows = data.split('\n').slice(1);
    const movies = rows.map(row => {
        const [title, releaseyear, duration, rating, genres, language, directors, maincast, plotsummary, imageurl, reviews1, reviews2, reviews3] = row.split('|');
        return { title, releaseyear, duration, rating, genres, language, directors, maincast, plotsummary, imageurl,reviews1, reviews2, reviews3 };
    });
    return movies;
}


function showMovies(movies) {
    main.innerHTML = "";
    movies.forEach(movie => {
        const { title, releaseyear, duration, rating, genres, language, directors, maincast, plotsummary, imageurl, reviews1, reviews2, reviews3 } = movie;

        const movieEl = document.createElement("div");
        movieEl.classList.add("card");

        movieEl.innerHTML = `
            <div class="info">
                <h3>${title}</h3><br><br>
                <img src="${imageurl}" alt="${title}"><br>
                <div><strong>Release Year:</strong> ${releaseyear}</div>
                <div><strong>Duration:</strong> ${duration} minutes</div>
                <div><strong>Rating:</strong> ${rating}</div>
                <div><strong>Genres:</strong> ${genres}</div><br>
                <div><strong>Language:</strong> ${language}</div><br>
                <div><strong>Directors:</strong> ${directors}</div><br>
                <div><strong>Cast:</strong> ${maincast}</div><br>
                <div><strong>Summary:</strong> ${plotsummary}</div><br>
                <div><strong>Others thought:</strong><br><br> ${reviews1}</div><br>
                <div> ${reviews2}</div><br>
                <div> ${reviews3}</div><br>
                <form id="ratingForm-${title}">
                    <label for="rating-${title}">Rate this movie (0-10): </label>
                    <input type="number" id="rating-${title}" name="rating" min="0" max="10" step="0.1">
                    <button type="button" onclick="submitRating('${title}')">Submit Rating</button>
                </form>
                
            </div>
        `;

        main.appendChild(movieEl);
    });
}
let userRatings = {};


// Function to handle rating submission
function submitRating(movieTitle) {
    const ratingInput = document.getElementById(`rating-${movieTitle}`).value;

    // Store rating in dictionary
    userRatings[movieTitle] = parseFloat(ratingInput);

    // Log userRatings for testing (remove this line in production)
    console.log('User Ratings:', userRatings);
    
    // Call a function to handle further processing (if needed)
    handleRatingSubmission();
}

// Function to handle further processing after rating submission
function handleRatingSubmission() {
    var userRatingsArray = Object.entries(userRatings);

// Sort the array based on the values
    userRatingsArray.sort(function(a, b) {
       return a[1] - b[1]; // Change this if values are not numeric
    });
    console.log(userRatingsArray)
    function getRatingByTitle(title) {
        for (var i = 0; i < userRatingsArray.length; i++) {
            if (userRatingsArray[i][0] === title) {
                return userRatingsArray[i][1];
            }
        }
        // Return null if title not found
        return null;
    }
    var highestmovies = userRatingsArrayrray.slice(0, -2);
    if((getRatingByTitle(highestmovies[1])-getRatingByTitle(highestmovies[0]))>3){
        return get_recommendations(highestmovies[1])
    }
    else{
        var arr1=get_recommendations(highestmovies[1]).splice(0,4)
        var arr2=get_recommendations(highestmovies[0]).splice(0,3)
        arr1= arr1.concat(arr2)
        uniqarr= Array.from(new Set(arr1))
        uniqarr=uniqarr.splice(0,5)
        return uniqarr.sort(function(a, b) {
            return a[1] - b[1]; 
         });
    }

}

form.addEventListener("submit", (e) => {
    e.preventDefault();

    const searchTerm = search.value.trim().toLowerCase();
    if (searchTerm) {
        searchMovies(searchTerm);
        search.value = "";
    }
});

async function searchMovies(searchTerm) {
    const response = await fetch(CSV);
    const data = await response.text();
    const movies = processData(data);

    const filteredMovies = movies.filter((el) => {
        return el.title.toLowerCase().includes(searchTerm);
    });

    showMovies(filteredMovies);
}

const formatData = movies => {
    let formatted = [];
  
    for (const [key, labels] of Object.entries(movies)) {
      let tmpObj = {};
      const desc = labels.map(l => {
        return l.description.toLowerCase();
      });
  
      tmpObj = {
        id: key,
        content: desc.join(" ")
      };
  
      formatted.push(tmpObj);
    }
  
    return formatted;
  };

// Function to extract relevant features from data
function relevant(movies) {
    let relevantFeatures = [];
    for (let i = 0; i < movies.length; i++) {
        relevantFeatures.push(movies[i]['title'] + ' ' + movies[i]['directors'] + ' ' + movies[i]['genres'] + ' ' + movies[i]['plotsummary']+movies[i]['language']);
    }
    return relevantFeatures;

}

movies.forEach(item => {
    item['relevant_features'] = relevant([item]);
});
function calculateTF(wordDict, tokenizedText) {
    let tfDict = {};
    const textLength = tokenizedText.length;
    for (let word in wordDict) {
        tfDict[word] = wordDict[word] / textLength;
    }
    return tfDict;
}

// Calculate Inverse Document Frequency (IDF)
function calculateIDF(docs) {
    let idfDict = {};
    const N = docs.length;

    docs.forEach(doc => {
        for (let word in doc) {
            if (doc[word] > 0) {
                idfDict[word] = idfDict[word] ? idfDict[word] + 1 : 1;
            }
        }
    });
    for (let word in idfDict) {
        idfDict[word] = Math.log(N / idfDict[word]);
    }

    return idfDict;
}

