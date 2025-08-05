const express = require('express');
const fs = require('fs');
const path = require('path');
const bodyParser = require('body-parser');
const cors = require('cors');
const app = express();
const PORT = 8081;

app.use(bodyParser.urlencoded({ extended: true }));
app.use(bodyParser.json());
app.use(cors({
  methods: ['GET', 'POST', 'DELETE', 'PUT']
}));

const classesDir = path.join(__dirname, 'data');

// Route for the root path
app.get('/', (req, res) => {
  res.send('Welcome to the Class Directory API. Use /api/classes to get the list of classes and /api/search to search for students.');
});
console.log('Classes Directory:', classesDir);
if (!fs.existsSync(classesDir)) {
  console.error('Classes directory does not exist:', classesDir);
  return res.status(500).json({ message: 'Classes directory does not exist' });
}

// Utility function to read and search students in a specific class/semester file
function searchStudent(classID, semester, filePath, searchQuery) {
  const { firstName, lastName, studentID, email } = searchQuery;
  const data = fs.readFileSync(filePath, 'utf8');
  const students = data.split('\n').filter(Boolean);
  let results = [];

  students.forEach(studentLine => {
    const details = studentLine.split(',').map(field => field.trim());
    const [studentLastName, studentFirstName, studentIDFromFile, ...studentEmails] = details;

    const matches = (!firstName || studentFirstName.toLowerCase() === firstName.toLowerCase()) &&
                    (!lastName || studentLastName.toLowerCase() === lastName.toLowerCase()) &&
                    (!studentID || studentIDFromFile === studentID) &&
                    (!email || studentEmails.some(e => e.toLowerCase() === email.toLowerCase()));

    if (matches) {
      results.push({
        classID,
        semester,
        studentFirstName,
        studentLastName,
        studentID: studentIDFromFile,
        studentEmails
      });
    }
  });

  return results;
}

// Route to search for students across all classes
app.get('/api/search', (req, res) => {
  const { firstName, lastName, studentID, email } = req.query;

  if (!firstName && !lastName && !studentID && !email) {
    return res.status(400).json({ message: 'Please provide at least one search criterion' });
  }

  let allResults = [];

  fs.readdir(classesDir, (err, classIDs) => {
    if (err) return res.status(500).json({ message: 'Error reading classes directory' });

    classIDs.forEach(classID => {
      const classPath = path.join(classesDir, classID);
      fs.readdirSync(classPath).forEach(file => {
        const semester = path.basename(file, '.txt');
        const filePath = path.join(classPath, file);
        const results = searchStudent(classID, semester, filePath, req.query);
        allResults = allResults.concat(results);
      });
    });

    if (allResults.length > 0) {
      res.json(allResults);
    } else {
      res.status(404).json({ message: 'No students found matching the search criteria' });
    }
  });
});

// Route to list all classes
app.get('/api/classes', (req, res) => {
  fs.readdir(classesDir, (err, classIDs) => {
    if (err) {
	console.error('Error reading classes directory:', err); // Log the error
	return res.status(500).json({ message: 'Error reading classes directory' });
  }
    res.json(classIDs);
  });
});

// Route to list semesters for a given class
app.get('/api/classes/:classID/semesters', (req, res) => {
  const classPath = path.join(classesDir, req.params.classID);
  fs.readdir(classPath, (err, files) => {
    if (err) return res.status(404).json({ message: 'Class not found' });
    const semesters = files.map(file => path.basename(file, '.txt'));
    res.json(semesters);
  });
});

// Route to list students for a given class and semester
app.get('/api/classes/:classID/semesters/:semester/students', (req, res) => {
  const filePath = path.join(classesDir, req.params.classID, `${req.params.semester}.txt`);
  fs.readFile(filePath, 'utf8', (err, data) => {
    if (err) return res.status(404).json({ message: 'Semester not found' });

    const students = data.split('\n').filter(Boolean).map(student => {
      const details = student.split(',').map(field => field.trim());
      return {
        lastName: details[0],
        firstName: details[1],
        studentID: details[2],
        email: details.slice(3)
      };
    });

    res.json(students);
  });
});


// Route to add a student to a class/semester
// Route to add a student to a class/semester
app.post('/api/classes/:classID/semesters/:semester/students', async (req, res) => {
    const { firstName, lastName, email, studentID } = req.body; // Extracting data from the request body
    const filePath = path.join(classesDir, req.params.classID, `${req.params.semester}.txt`);

    // Check for missing fields
    if (!firstName || !lastName || !studentID || !email) { // Ensure all fields are checked
        return res.status(400).json({ message: 'All fields are required' });
    }

    // Construct the student info string
    const studentInfo = `${lastName},${firstName},${studentID},${email}`; // Use the email directly

    // Append the student information to the file
    fs.appendFile(filePath, `\n${studentInfo}`, err => {
        if (err) {
            console.error('Error writing to file:', err); // Log the error
            return res.status(500).json({ message: 'Error adding student', error: err.message });
        }
        res.json({ message: 'Student added successfully' });
    });
});



// Route to remove a student from a class/semester
app.delete('/api/classes/:classID/semesters/:semester/students/:studentID', async (req, res) => {
    const { classID, semester, studentID } = req.params; // Extract classID, semester, and studentID from request parameters
    const filePath = path.join(classesDir, classID, `${semester}.txt`);

    try {
        // Read the current contents of the file
        const data = await fs.promises.readFile(filePath, 'utf-8');
        const lines = data.split('\n'); // Split the file into lines

        // Filter out the student entry that matches the studentID
        const filteredLines = lines.filter(line => {
            const studentInfo = line.split(','); // Assuming the format is lastName,firstName,studentID,email
            return studentInfo[2] !== studentID; // studentID is the third item (index 2)
        });

        // Write the remaining student entries back to the file
        await fs.promises.writeFile(filePath, filteredLines.join('\n'), 'utf-8');

        res.json({ message: 'Student removed successfully' });
    } catch (error) {
        console.error('Error removing student:', error);
        res.status(500).json({ message: 'Error removing student', error: error.message });
    }
});

// Route to update a student's information
// Route to update a student's information
app.put('/api/classes/:classID/semesters/:semester/students/:studentID', async (req, res) => {
    const { firstName, lastName, email } = req.body;
    const { classID, semester, studentID } = req.params;
    const filePath = path.join(classesDir, classID, `${semester}.txt`);

    // Validate the request
    if (!firstName || !lastName || !email || !studentID) {
        return res.status(400).json({ message: 'All fields are required' });
    }

    // Read the existing student data
    fs.readFile(filePath, 'utf8', (err, data) => {
        if (err) {
            return res.status(500).json({ message: 'Error reading student data' });
        }

        const students = data.split('\n').map(line => {
            const [lastName, firstName, studentID, email] = line.split(',');
            return { 
                lastName, 
                firstName, 
                studentID, 
                email: email ? email.split(', ') : [] // Safeguard against undefined email
            };
        });

        // Find the student to update
        const studentIndex = students.findIndex(student => student.studentID === studentID);
        if (studentIndex === -1) {
            return res.status(404).json({ message: 'Student not found' });
        }

        // Update the student information
        students[studentIndex] = {
            lastName,
            firstName,
            studentID,
            email: [email], // Assuming one email for now; adjust as necessary
        };

        // Write the updated student data back to the file
        const updatedData = students.map(student => `${student.lastName},${student.firstName},${student.studentID},${student.email.join(', ')}`).join('\n');

        fs.writeFile(filePath, updatedData, 'utf8', (err) => {
            if (err) {
                return res.status(500).json({ message: 'Error updating student information' });
            }
            res.json({ message: 'Student information updated successfully' });
        });
    });
});
       
// Route to add a new semester to a class
// Route to add a new semester to a class
app.post('/api/classes/:classID/semesters', (req, res) => {
  const { semester } = req.body;
  const classPath = path.join(classesDir, req.params.classID);

  console.log('Received request to add semester:', semester, 'to class:', req.params.classID);

  // Check if the semester value is provided
  if (!semester) {
    console.error('No semester provided');
    return res.status(400).json({ message: 'Semester is required' });
  }

  // Check if the class directory exists
  if (!fs.existsSync(classPath)) {
    console.error('Class ID does not exist:', req.params.classID);
    return res.status(404).json({ message: 'Class ID does not exist.' });
  }

  // Define the path for the new semester file
  const filePath = path.join(classPath, `${semester}.txt`);

  // Check if the semester file already exists
  if (fs.existsSync(filePath)) {
    console.error('Semester already exists:', semester);
    return res.status(400).json({ message: 'Semester already exists.' });
  }

  // Create a new file for the semester
  fs.writeFile(filePath, '', err => {
    if (err) {
      console.error('Error creating new semester:', err);
      return res.status(500).json({ message: 'Error creating new semester' });
    }
    console.log('New semester created successfully:', semester);
    res.json({ message: 'New semester created successfully' });
  });
});

// Route to add a new class
app.post('/api/classes', (req, res) => {
  const { classID } = req.body;

  if (!classID) return res.status(400).json({ message: 'Class ID is required' });

  const classPath = path.join(classesDir, classID);
  fs.mkdir(classPath, err => {
    if (err) return res.status(500).json({ message: 'Error creating new class directory' });
    res.json({ message: 'New class created successfully' });
  });
});

// Start the server
app.listen(PORT, () => {
  console.log(`Server is running on http://localhost:${PORT}`);
});
