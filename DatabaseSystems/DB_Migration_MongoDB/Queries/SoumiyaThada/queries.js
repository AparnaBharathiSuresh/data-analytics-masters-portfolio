// Find movies with a specific keyword
db.movie_metadata.find({"keywords.name":{$regex:/jealousy/i}},{title:1,_id:0})

// Find movies with a specific runtime range
db.movie_metadata.find({runtime:{$gte:120,$lte:180}},{title:1,runtime:1,_id:0})

// Find movies with any of the spoken language
db.movie_metadata.find({ "spoken_languages.name": { $in: ["English", "Deutsch"] } },{title:1,_id:0,"spoken_languages.name":1})

// Find movies where a specific actor is part of the cast and the genre is action
db.movie_metadata_trial.find({ "cast.name": "Tom Hanks", "genres.name": "Action" },{title:1,_id:0})

// Find movies where the title contains a number
db.movie_metadata.find({ title: { $regex: /\d+/ } }, {title:1,_id:0})

// Find the top 5 longest movies
db.movie_metadata.find({},{title:1,_id:0,runtime:1}).sort({ runtime: -1 }).limit(5)

// Aggregate Queries

// Top 10 movies based on revenue generated
db.movie_metadata.aggregate([
  { $sort: { revenue: -1 } }, 
  { $limit: 10 }, 
  { 
    $project: { 
      _id: 0, 
      title: 1, 
      revenue: { $divide: ["$revenue", 1000000] }, 
      budget: { $divide: ["$budget", 1000000] },
      profit: { $divide: [{ $subtract: ["$revenue", "$budget"] }, 1000000] } 
    } 
  } 
])

// Number of Movies in each genre
db.movie_metadata.aggregate([
  { $unwind: "$genres" }, 
  { 
    $group: { 
      _id: "$genres.name", 
      count: { $sum: 1 } 
    } 
  }
])

// Find the top 10 actors/actresses with the most movie appearances
db.movie_metadata_trial.aggregate([
  { $unwind: "$cast" }, 
  { 
    $group: { 
      _id: "$cast.name", 
      count: { $sum: 1 } 
    } 
  },
  { $sort: { count: -1 } }, 
  { $limit: 10 } 
])

// Find movies with average rating greater than 4
db.movie_metadata_trial_aparna.aggregate([
  {
    $project: {
      title: 1,
      averageRating: { $avg: "$ratings.rating" } 
    }
  },
  {
    $match: {
      averageRating: { $gte: 4 } 
    }
  }
])


