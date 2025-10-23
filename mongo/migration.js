db = db.getSiblingDB('cafe_mongo');

db.feedback.insertMany([
  {
    order_id: 1,
    customer_id: 1,
    rating: 5,
    comment: "Капучино отличный, обслуживание быстрое!",
    sentiment: 5, // максимальная положительная оценка
    date: new Date()
  },
  {
    order_id: 2,
    customer_id: 2,
    rating: 4,
    comment: "Десерт вкусный, но кофе остыл.",
    sentiment: 3, // нейтральный отзыв
    date: new Date()
  }
]);

db.order_history.insertOne({
  order_id: 1,
  status_changes: [
    { status: "created", timestamp: new Date(Date.now() - 600000) },
    { status: "paid", timestamp: new Date(Date.now() - 500000) },
    { status: "completed", timestamp: new Date() }
  ]
});

print("MongoDB initialized successfully!");
