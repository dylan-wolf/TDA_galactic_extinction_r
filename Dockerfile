FROM ubuntu:20.04
ENV DEBIAN_FRONTEND=noninteractive


# Install dependencies
RUN apt-get update && apt-get install -y \
    cmake \
    g++ \
    qtbase5-dev \
    libboost-all-dev \
    libeigen3-dev \
    doxygen \
    git

# Clone and build RIVET
RUN git clone https://github.com/rivetTDA/rivet.git /opt/rivet
WORKDIR /opt/rivet
RUN mkdir build && cd build && cmake .. -DBUILD_TESTING=OFF && make

# Set entrypoint to the rivet_console command (adjust as needed)
WORKDIR /opt/rivet/build
ENTRYPOINT ["./rivet_console"]
