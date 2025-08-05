#Find a movie by title The Matrix:
db.movie_metadata.find({title: "The Matrix"})

#Find movies released after 2000-01-01
db.movie_metadata.find({release_date: {$gt: "2000-01-01"}})

#Find movies that are either a Drama or Thriller.
db.movie_metadata.find({ "genres.name": { $in: ["Drama", "Thriller"] } })

#Find movies with a specific keyword – “artificial intelligence”
db.movie_metadata.find({"keywords.name": "artificial intelligence"})

#Find ratings and the movies given the by user with id 18.
db.movie_metadata.find({"ratings.userId": 18}, { title: 1, "ratings.$": 1 ,_id : 0})

#Aggregation Queries:
#Total number of ratings the movie Toy Story has got:
db.movie_metadata.aggregate([
  {
    $match: { "title": "Toy Story" } 
  },
  {
    $unwind: "$ratings" 
  },
  {
    $group: {
      _id: "$title", 
      numberOfRatings: { $sum: 1 } 
    }
  }
])

#Total number of movies released from 2000-2020:
db.movie_metadata.aggregate([
 	{ 
    $match: { release_date: { $gte: "2000-01-01", $lte: "2020-12-31" } } 
},
{
  $group: { _id: null, count: { $sum: 1 } } 
},
{ 
 $project: { _id: 0  } 
}
] )

#Find movies with the highest number of ratings
db.movie_metadata.aggregate([
  {
    $match: {
      ratings: { $ne: null } 
    }
  },
  {
    $project: {
      title: 1,
      numberOfRatings: { $size: "$ratings" } 
    }
  },
  {
    $sort: { numberOfRatings: -1 } 
  },
  {
    $limit: 10 
  }
])

#Number of movies in each genre and sort by highest genre movies.
db.movie_metadata.aggregate([
  {
    $unwind: "$genres
  },
  {
    $group: {
      _id: "$genres.name", 
      totalMovies: { $sum: 1 } 
    }
  },
  {
    $project: {
      genre: "$_id", 
      totalMovies: 1
      _id: 0 
    }
  },
  {
    $sort: { totalMovies: -1 } 
  }
])

#Total count of movies:
db.movie_metadata.aggregate([ { $count: "totalMovies" }] )

#Total cast and crew:
db.movie_metadata.aggregate([
  {
    $match: {
      $and: [
        { cast: { $ne: null } }, // Filter out documents where cast is null
        { crew: { $ne: null } }  // Filter out documents where crew is null
      ]
    }
  },
  {
    $project: {
      totalCast: { $size: "$cast" }, // Calculate the size of the cast array
      totalCrew: { $size: "$crew" }  // Calculate the size of the crew array
    }
  },
  {
    $group: {
      _id: null, // Group all documents together
      totalCast: { $sum: "$totalCast" }, // Sum the totalCast values
      totalCrew: { $sum: "$totalCrew" }  // Sum the totalCrew values
    }
  }
])

#Total Keywords:
db.movie_metadata.aggregate([
  {
    $unwind: "$keywords" // Unwind the keywords array
  },
  {
    $group: {
      _id: null, // Group all documents together
      totalKeywords: { $sum: 1 } // Count the total number of keywords
    }
  }
])


