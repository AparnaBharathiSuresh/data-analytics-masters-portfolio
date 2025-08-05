const express = require('express');
const fs = require('fs');
const path = require('path');
const app = express();
const PORT = 8081;

const classesDir = path.join(__dirname, 'classes');
function renderMainPage(title, content) {
    return `
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>${title}</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 0; padding: 0; background-color: #faf3e0; color: #333; }
            header { background-color: #4682b4; color: white; padding: 10px 20px; text-align: center; }
            main { padding: 20px; }
            h1 { font-size: 2em; }
            ul { list-style-type: none; padding: 0; }
            li { margin: 5px 0; }
            a { text-decoration: none; color: #4682b4; }
            a:hover { text-decoration: underline; }
            .search-container { margin: 20px 0; padding: 10px; background-color: #f9f9f9; border-radius: 5px; }
            .search-container input[type="text"] { padding: 8px; width: 200px; margin-right: 10px; }
            .search-container button { padding: 8px 16px; background-color: #007BFF; color: white; border: none; border-radius: 5px; cursor: pointer; }
            .search-container button:hover { background-color: #0056b3; }
        </style>
    </head>
    <body>
        <header>
            <h1>Welcome to the Class Directory</h1>
        </header>
        <main>
            <h2>Navigate to:</h2>
            <ul>
                ${content}
            </ul>
            <div>
                <a href="/search"><button>Search</button></a>
            </div>
        </main>
    </body>
    </html>
    `;
}

// Helper function to render the search page
function renderSearchPage() {
    return `
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Search</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 0; padding: 0; background-color: #faf3e0; color: #333; }
            .search-container { margin: 20px 0; padding: 10px; background-color: #f9f9f9; border-radius: 5px; }
            .search-container input[type="text"] { padding: 8px; width: 200px; margin-right: 10px; }
            .search-container button { padding: 8px 16px; background-color: #007BFF; color: white; border: none; border-radius: 5px; cursor: pointer; }
            .search-container button:hover { background-color: #0056b3; }
        </style>
    </head>
    <body>
        <h1>Search</h1>
        <form action="/search/results" method="GET">
            <div>
                <label for="firstName">First Name:</label>
                <input type="text" id="firstName" name="firstName"><br>
            </div>
            <div>
                <label for="lastName">Last Name:</label>
                <input type="text" id="lastName" name="lastName"><br>
            </div>
            <div>
                <label for="studentID">Student ID:</label>
                <input type="text" id="studentID" name="studentID"><br>
            </div>
            <div>
                <label for="email">Email ID:</label>
                <input type="text" id="email" name="email"><br>
            </div>
            <button type="submit">Search</button>
        </form>
    </body>
    </html>
    `;
}

app.use((req, res, next) => {
    console.log("Request received:", req.url);
    next();
});


app.get('/search', (req, res) => {
    res.send(renderSearchPage()); 
});

app.get('/search/results', (req, res) => {
    const { firstName, lastName, studentID, email } = req.query;

    console.log("Search initiated with query parameters:", req.query);

    // Check for valid search criteria
    if (!firstName && !lastName && !studentID && !email) {
        return res.status(400).send('Please provide at least one search criterion.');
    }

    let results = []; // This will hold the search results

    // Function to search students in each file
    function searchStudent(classID, semester, filePath) {
        console.log('Reading file:', filePath);
        const data = fs.readFileSync(filePath, 'utf8');
        console.log('File content:', data);

        const students = data.split('\n').filter(Boolean); // Split by line and filter out empty lines

        students.forEach(studentLine => {
            console.log('Processing student line:', studentLine);

            const details = studentLine.split(',').map(field => field.trim());
            const [studentLastName, studentFirstName, studentIDFromFile, ...studentEmails] = details;

            // Match logic with trimmed fields
            const matches = (!firstName || studentFirstName.toLowerCase() === firstName.trim().toLowerCase()) &&
                            (!lastName || studentLastName.toLowerCase() === lastName.trim().toLowerCase()) &&
                            (!studentID || studentIDFromFile.trim() === studentID.trim()) &&
                            (!email || studentEmails.some(emailAddr => emailAddr.toLowerCase() === email.trim().toLowerCase()));
            console.log('Matching line?', matches);

            if (matches) {
                results.push({
                    studentLastName,
                    studentFirstName,
                    studentID: studentIDFromFile,
                    studentEmails,
                    classID,
                    semester
                });
            }
        });
    }

    fs.readdir(classesDir, (err, classIDs) => {
        if (err) return res.status(500).send('Error reading classes directory');

        classIDs.forEach(classID => {
            const classPath = path.join(classesDir, classID);
            fs.readdirSync(classPath).forEach(file => {
                const semester = path.basename(file, '.txt');
                const filePath = path.join(classPath, file);
                searchStudent(classID, semester, filePath);
            });
        });

        if (results.length > 0) {
            let content = `
                <h2>Search Results</h2>
                <style>
                    table {
                        width: 100%;
                        border-collapse: collapse;
                        margin-top: 20px;
                    }
                    th, td {
                        border: 1px solid #ccc;
                        padding: 10px;
                        text-align: left;
                    }
                    th {
                        background-color: #4682b4;
                        color: white;
                    }
                    tr:nth-child(even) {
                        background-color: #f2f2f2;
                    }
                </style>
                <table>
                    <thead>
                        <tr>
                            <th>First Name</th>
                            <th>Last Name</th>
                            <th>Student ID</th>
                            <th>Email(s)</th>
                            <th>Class</th>
                            <th>Semester</th>
                        </tr>
                    </thead>
                    <tbody>`;
            results.forEach(result => {
                content += `
                    <tr>
                        <td>${result.studentFirstName}</td>
                        <td>${result.studentLastName}</td>
                        <td>${result.studentID}</td>
                        <td>${result.studentEmails.join(', ')}</td>
                        <td>${result.classID}</td>
                        <td>${result.semester}</td>
                    </tr>`;
            });
            content += `
                    </tbody>
                </table>`;

            res.send(content);
        } else {
            console.log('No students found matching the search criteria.');
            res.status(404).send('No students found matching the search criteria.');
        }
    });
});

// Route to list all class IDs
app.get('/', (req, res) => {
    fs.readdir(classesDir, (err, classIDs) => {
        if (err) return res.status(500).send('Error reading classes directory');
        let content = '<ul>';
        classIDs.forEach(classID => {
            content += `<li><a href="/${classID}">${classID}</a></li>`;
        });
        content += '</ul>';
        const html = renderMainPage('Class Directory', content);
        res.send(html);
    });
});

// Route to list semesters under class
app.get('/:classID', (req, res) => {
    const classPath = path.join(classesDir, req.params.classID);
    fs.readdir(classPath, (err, files) => {
        if (err) return res.status(404).send('Class ID not found');
        let content = '<ul>';
        files.forEach(file => {
            const fileName = path.basename(file, '.txt');
            content += `<li><a href="/${req.params.classID}/${fileName}">${fileName}</a></li>`;
        });
        content += '</ul>';

        const html = renderMainPage(`Files for Class ${req.params.classID}`, content);
        res.send(html);
    });
});

// Route to list students in a class/semester
app.get('/:classID/:semester', (req, res) => {
    const filePath = path.join(classesDir, req.params.classID, `${req.params.semester}.txt`);
    fs.readFile(filePath, 'utf8', (err, data) => {
        if (err) return res.status(404).send('File not found');
        const students = data.split('\n').filter(Boolean);
        let content = `
            <h2>Students in ${req.params.classID} (${req.params.semester})</h2>
            <style>
                table {
                    width: 100%;
                    border-collapse: collapse;
                    margin-top: 20px;
                }
                th, td {
                    border: 1px solid #ccc;
                    padding: 10px;
                    text-align: left;
                }
                th {
                    background-color: #4682b4;
                    color: white;
                }
                tr:nth-child(even) {
                    background-color: #f2f2f2;
                }
            </style>
            <table>
                <thead>
                    <tr>
                        <th>Last Name</th>
                        <th>First Name</th>
                        <th>Student ID</th>
                        <th>Email(s)</th>
                    </tr>
                </thead>
                <tbody>`;
        
        students.forEach(student => {
            const details = student.split(',').map(field => field.trim());
            const studentLastName = details[0];
            const studentFirstName = details[1];
            const studentID = details[2];
            const studentEmails = details.slice(3);

            content += `
                <tr>
                    <td>${studentLastName}</td>
                    <td>${studentFirstName}</td>
                    <td>${studentID}</td>
                    <td>${studentEmails.join(', ')}</td>
                </tr>`;
        });
        content += `
                </tbody>
            </table>`;

        res.send(content);
    });
});

// Start the server
app.listen(PORT, () => {
    console.log(`Server is running at http://localhost:${PORT}`);
});
