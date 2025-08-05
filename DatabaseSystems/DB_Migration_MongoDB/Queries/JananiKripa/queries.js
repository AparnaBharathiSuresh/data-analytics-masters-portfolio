// 1. Find all comedy movies. 
db.movie_metadata.find({ 'keywords.name': 'comedy'  },  { title: 1, _id : 0 }).sort({title: 1})

// 2. Get the cast and crew of Ariel movie. 
db.movie_metadata.findOne({ "title": "Ariel" }, { "cast": 1, "crew": 1, "_id": 0 })

// 3. Top 10 movies based on revenue generated 
db.movie_metadata.find({},{title: 1, revenue: 1, _id: 0}).sort({ "revenue": -1 }).limit(10)

// 4. Top 15 keywords
db.movie_metadata.aggregate([  { $unwind: "$keywords" },   { $group: { _id: "$keywords.name", count: { $sum: 1 } } },  { $sort: { count: -1 } },   { $limit: 15 } ])

// 5. Get the average rating of movies and order by highly rated movies. 
db.movie_metadata.aggregate([  {    $group: {      _id: "$title",      average_rating: { $avg: "$vote_average" }    }  },  { $sort: { average_rating: -1 } }])

// 6. Update status after a movie release
db.movie_metadata.updateOne(   { "id": 12345 },   { $set: { "status": "Released" } } )

// 7. Count the number of movies released each year:
db.movie_metadata.aggregate([ { $group: { _id: { $year: { $toDate: "$release_date" } }, count: { $sum: 1 } } }, { $sort: { _id: 1 }} ]) 

// 8. Get the number of movies in each language:
db.movie_metadata.aggregate([ {  $group: {   _id: "$original_language",   count: { $sum: 1 }  } }])

// 9. Calculate the average runtime of movies for each genre:
db.movie_metadata.aggregate([ { $unwind: "$genres" } , { $group: { _id: "$genres.name", average_runtime: { $avg:"$runtime" } } } ])
