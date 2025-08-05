import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import SearchComponent from './searchcomponent';
import ClassDirectory from './ClassDirectory';
import SearchResults from './SearchResults';
import StudentDetails from './StudentDetails';
import SemesterManagement from './SemesterManagement';
import 'bootstrap/dist/css/bootstrap.min.css';
import './App.css';

const App: React.FC = () => {
  return (
    <Router>
      <div className="container">
        <h1 className="my-4 text-center">Class Directory</h1>
        <Routes>
          <Route path="/" element={
            <div className="text-center">
              <h2>Welcome to the Class Directory</h2>
              <a href="/classes" className="btn btn-primary mt-3">View Class Directory</a>
              <br />
              <a href="/search" className="btn btn-primary mt-3">Go to Search</a>
            </div>
          } />
          <Route path="/classes" element={<ClassDirectory />} />
          <Route path="/classes/:classID" element={<SemesterManagement />} />
          <Route path="/student/:semester/:classID" element={<StudentDetails />} /> {/* Ensure correct path */}
          <Route path="/search" element={<SearchComponent />} />
          <Route path="/search-results" element={<SearchResults />} />
          <Route path="*" element={
            <div className="text-center">
              <h2>404 - Not Found</h2>
              <a href="/" className="btn btn-secondary mt-3">Back to Home</a>
            </div>
          } />
        </Routes>
      </div>
    </Router>
  );
};

export default App;
