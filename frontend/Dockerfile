# Use an official Nginx image as the base image
FROM nginx:alpine

# Set the working directory to /usr/share/nginx/html
WORKDIR /usr/share/nginx/html

# Remove default Nginx static files
RUN rm -rf /usr/share/nginx/html/*

# Copy static files (HTML, CSS, JS) from your build context to the working directory
COPY . .

# Install gettext to use envsubst
RUN apk add --no-cache gettext

# Copy the startup script
COPY start.sh /start.sh
RUN chmod +x /start.sh

# Set ownership of the files to nginx user for better security (optional)
RUN chown -R nginx:nginx /usr/share/nginx/html

# Expose port 5500 to the outside world
EXPOSE 5500

# Start Nginx using the custom script
CMD ["/start.sh"]