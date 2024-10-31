// Open the Chatbot and display the initial message and predefined questions
function openChatbot() {
    // Display the chatbot container
    document.getElementById("chatbot-container").style.display = "flex";
    
    // Clear previous messages (if any) and add initial message and predefined questions
    document.getElementById("chatbot-messages").innerHTML = "";
    addMessage("Hi, how can I help you?", "bot-message");
    displayPredefinedQuestions();
}

// Close the Chatbot
function closeChatbot() {
    document.getElementById("chatbot-container").style.display = "none";
}

// Display predefined questions as clickable options
function displayPredefinedQuestions() {
    const questions = [
        "Provide a house between 3-4 cr",
        "Show properties with 3 bedrooms",
        "List houses with garden space"
    ];

    questions.forEach((question) => {
        const questionDiv = document.createElement("div");
        questionDiv.className = "predefined-question";
        questionDiv.innerText = question;

        questionDiv.onclick = function() {
            addMessage(question, "user-message");

            if (question === "Provide a house between 3-4 cr") {
                showListingsForPriceRange(30000000, 40000000);
            } else if (question === "Show properties with 3 bedrooms") {
                showListingsForFeature("3 Bedrooms");
            } else if (question === "List houses with garden space") {
                showListingsForFeature("Garden Space");
            }
        };

        document.getElementById("chatbot-messages").appendChild(questionDiv);
    });
}

// Add a message to the chat
function addMessage(message, type) {
    const messageDiv = document.createElement("div");
    messageDiv.className = type;
    messageDiv.innerText = message;
    document.getElementById("chatbot-messages").appendChild(messageDiv);
    document.getElementById("chatbot-messages").scrollTop = document.getElementById("chatbot-messages").scrollHeight;
}

// Display listings based on price range directly in the chatbot
function showListingsForPriceRange(minPrice, maxPrice) {
    const listingchatbot = [
        { title: "House at Soaltee mode", price: 35000000, cprice: "3.5 Crore", image: "static/image/House_List/House1/House1a.jpg", link: "/house1" },
        { title: "House at Bafal", price: 32000000, cprice: "3.2 Crore", image: "static/image/House_List/House2/House2a.jpg", link: "/house1" },
        { title: "Luxury House at Lazimpat", price: 38000000, cprice: "3.8 Crore", image: "static/image/House_List/House3/House3a.jpg", link: "/house1" }
    ];

    // Filter listings based on price range
    const filteredListings = listingchatbot.filter(listing => listing.price >= minPrice && listing.price <= maxPrice);
    addMessage("The available options are:", "bot-message");

    filteredListings.forEach(listing => {
        const listingDiv = document.createElement("div");
        listingDiv.className = "listingchatbot-card";

        const image = document.createElement("img");
        image.src = listing.image;
        listingDiv.appendChild(image);

        const infoDiv = document.createElement("div");
        infoDiv.className = "listingchatbot-info";

        const title = document.createElement("p");
        title.className = "listingchatbot-title";
        title.innerText = listing.title;
        infoDiv.appendChild(title);

        const cprice = document.createElement("p");
        cprice.className = "listing-price"; // Updated class name
        cprice.innerText = `Price: Rs ${listing.cprice}`;
        infoDiv.appendChild(cprice);

        // Add a clickable link to view more details
        const link = document.createElement("a");
        link.href = listing.link;
        link.innerText = "View Details";
        link.target = "_blank";  // Opens in a new tab
        link.className = "view-details-link";
        infoDiv.appendChild(link);

        listingDiv.appendChild(infoDiv);
        document.getElementById("chatbot-messages").appendChild(listingDiv);
    });

    document.getElementById("chatbot-messages").scrollTop = document.getElementById("chatbot-messages").scrollHeight;
}


