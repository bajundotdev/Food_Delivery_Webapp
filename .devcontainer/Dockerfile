# Use Ubuntu 20.04 as the base image
FROM ubuntu:20.04

ENV DEBIAN_FRONTEND=noninteractive

# Install necessary packages:
# - mysql-workbench: the GUI app
# - fluxbox: a lightweight window manager
# - tigervnc-standalone-server: VNC server
# - x11-apps: useful X utilities (optional, for testing)
RUN wget https://dev.mysql.com/get/mysql-apt-config_0.8.24-1_all.deb && \
    DEBIAN_FRONTEND=noninteractive dpkg -i mysql-apt-config_0.8.24-1_all.deb && \
    apt-get update && \
    apt-get install -y mysql-workbench && \
    rm -rf /var/lib/apt/lists/*


# (Optional) Create a non-root user "vscode" and allow passwordless sudo.
RUN useradd -ms /bin/bash vscode && \
    echo "vscode ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers

# Switch to the non-root user
USER vscode
WORKDIR /home/vscode

# Expose VNC port (5901 by default)
EXPOSE 5901

# Create a startup script to launch the VNC server, window manager, and MySQL Workbench
RUN echo '#!/bin/bash\n\
export DISPLAY=:1\n\
# Start VNC server on display :1 with a geometry of 1280x800 and 24-bit colors\n\
tigervncserver :1 -geometry 1280x800 -depth 24\n\
# Give a moment for the VNC server to initialize\n\
sleep 5\n\
# Start a minimal window manager\n\
fluxbox &\n\
# Launch MySQL Workbench\n\
mysql-workbench\n\
# Once MySQL Workbench is closed, kill the VNC server\n\
tigervncserver -kill :1\n' > start.sh && chmod +x start.sh

# Run the startup script by default
CMD ["bash", "start.sh"]
