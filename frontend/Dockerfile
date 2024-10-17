# Use an official Nginx image as the base image
FROM nginx:alpine

# Set the working directory to /usr/share/nginx/html
WORKDIR /usr/share/nginx/html

# Remove default Nginx static files
RUN rm -rf /usr/share/nginx/html/*

# Copy static files (HTML, CSS, JS) from your build context to the working directory
COPY . .

# Set ownership of the files to nginx user for better security (optional)
RUN chown -R nginx:nginx /usr/share/nginx/html

# Expose port 80 to the outside world
EXPOSE 80

# Start Nginx server in the foreground to keep the container running
CMD ["nginx", "-g", "daemon off;"]