const notFound = (req, res, next) => {
  const error = new Error(`Not Found - ${req.originalUrl}`);
  error.status = 404; 
  res.status(404);
  next(error);
};

const errorHandlerMiddleWare = (err, req, res, next) => {
  if (res.headersSent) {
    return next(err); // avoid sending again if headers are already sent
  }

  const statusCode = err.status || (res.statusCode !== 200 ? res.statusCode : 500);
  res.status(statusCode).json({
    message: err.message,
    stack: process.env.NODE_ENV === 'production' ? null : err.stack,
  });
};


module.exports = {
  notFound,
  errorHandlerMiddleWare,
};
