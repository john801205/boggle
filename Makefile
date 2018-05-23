SOURCES = main.cpp

CXX = g++
CFLAGS = -std=c++11 -Wall -Wextra -Weffc++ -ggdb
TARGET = main

all: $(TARGET)

$(TARGET): $(SOURCES)
	$(CXX) $(CFLAGS) -o $(TARGET) $(SOURCES)

run: $(TARGET)
	./$(TARGET)

clean:
	rm -f $(TARGET)



