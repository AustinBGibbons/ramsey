// Independent exact verifier for a finite linear multicolour Ramsey prototype.
//
// Unlike the Python verifier, this implementation uses explicit ordered
// candidate vectors rather than bit masks.

#include <algorithm>
#include <cctype>
#include <fstream>
#include <iostream>
#include <sstream>
#include <stdexcept>
#include <string>
#include <vector>

namespace {

std::string trim(const std::string& input) {
    const auto first = std::find_if_not(
        input.begin(), input.end(),
        [](unsigned char ch) { return std::isspace(ch) != 0; });
    if (first == input.end()) {
        return "";
    }
    const auto last = std::find_if_not(
        input.rbegin(), input.rend(),
        [](unsigned char ch) { return std::isspace(ch) != 0; }).base();
    return std::string(first, last);
}

struct Prototype {
    int order = 0;
    std::vector<int> clique_sizes;
    std::string colors;
};

Prototype parse(const std::string& path) {
    std::ifstream input(path);
    if (!input) {
        throw std::runtime_error("cannot open prototype");
    }
    Prototype prototype;
    bool saw_order = false;
    bool saw_sizes = false;
    bool saw_colors = false;
    std::string raw;
    int line_number = 0;
    while (std::getline(input, raw)) {
        ++line_number;
        const auto comment = raw.find('#');
        if (comment != std::string::npos) {
            raw.erase(comment);
        }
        const std::string line = trim(raw);
        if (line.empty()) {
            continue;
        }
        std::istringstream stream(line);
        std::string key;
        std::string value;
        std::string extra;
        if (!(stream >> key >> value) || (stream >> extra)) {
            throw std::runtime_error("malformed record at line " +
                                     std::to_string(line_number));
        }
        if (key == "order" && !saw_order) {
            prototype.order = std::stoi(value);
            saw_order = true;
        } else if (key == "clique_sizes" && !saw_sizes) {
            std::stringstream values(value);
            std::string token;
            while (std::getline(values, token, ',')) {
                if (token.empty()) {
                    throw std::runtime_error("empty clique size");
                }
                prototype.clique_sizes.push_back(std::stoi(token));
            }
            saw_sizes = true;
        } else if (key == "colors" && !saw_colors) {
            prototype.colors = value;
            saw_colors = true;
        } else {
            throw std::runtime_error("unknown or duplicate key at line " +
                                     std::to_string(line_number));
        }
    }
    if (!saw_order || !saw_sizes || !saw_colors) {
        throw std::runtime_error("missing required record");
    }
    return prototype;
}

bool has_color(const Prototype& prototype, int left, int right, int color) {
    const int distance = right - left;
    return prototype.colors[static_cast<std::size_t>(distance - 1)] - '0' ==
           color;
}

bool descend(const Prototype& prototype, int color, int need,
             const std::vector<int>& candidates, std::vector<int>& chosen,
             std::vector<int>& witness, unsigned long long& nodes) {
    ++nodes;
    if (need == 0) {
        witness = chosen;
        return true;
    }
    if (static_cast<int>(candidates.size()) < need) {
        return false;
    }
    const int last_start = static_cast<int>(candidates.size()) - need;
    for (int index = 0; index <= last_start; ++index) {
        const int vertex = candidates[static_cast<std::size_t>(index)];
        std::vector<int> next;
        for (std::size_t later = static_cast<std::size_t>(index + 1);
             later < candidates.size(); ++later) {
            const int other = candidates[later];
            if (has_color(prototype, vertex, other, color)) {
                next.push_back(other);
            }
        }
        if (static_cast<int>(next.size()) < need - 1) {
            continue;
        }
        chosen.push_back(vertex);
        if (descend(prototype, color, need - 1, next, chosen, witness,
                    nodes)) {
            return true;
        }
        chosen.pop_back();
    }
    return false;
}

int verify(const Prototype& prototype) {
    if (prototype.order < 2 || prototype.clique_sizes.empty()) {
        std::cout << "INVALID\nreason invalid_parameters\n";
        return 1;
    }
    for (int size : prototype.clique_sizes) {
        if (size < 2) {
            std::cout << "INVALID\nreason invalid_clique_size\n";
            return 1;
        }
    }
    if (prototype.colors.size() !=
        static_cast<std::size_t>(prototype.order - 1)) {
        std::cout << "INVALID\nreason wrong_word_length\n";
        return 1;
    }
    for (char symbol : prototype.colors) {
        if (symbol < '1' ||
            symbol > static_cast<char>('0' + prototype.clique_sizes.size())) {
            std::cout << "INVALID\nreason invalid_color_symbol\n";
            return 1;
        }
    }

    std::vector<int> all_vertices;
    for (int vertex = 0; vertex < prototype.order; ++vertex) {
        all_vertices.push_back(vertex);
    }
    for (std::size_t color_index = 0;
         color_index < prototype.clique_sizes.size(); ++color_index) {
        std::vector<int> chosen;
        std::vector<int> witness;
        unsigned long long nodes = 0;
        const int color = static_cast<int>(color_index) + 1;
        if (descend(prototype, color, prototype.clique_sizes[color_index],
                    all_vertices, chosen, witness, nodes)) {
            std::cout << "INVALID\nreason forbidden_monochromatic_clique\n";
            std::cout << "color " << color << "\nvertices";
            for (int vertex : witness) {
                std::cout << ' ' << vertex;
            }
            std::cout << "\n";
            return 1;
        }
        std::cout << "color_" << color << "_search_nodes " << nodes << '\n';
    }

    bool cyclic_reflection = true;
    for (int distance = 1; distance < prototype.order; ++distance) {
        if (prototype.colors[static_cast<std::size_t>(distance - 1)] !=
            prototype.colors[
                static_cast<std::size_t>(prototype.order - distance - 1)]) {
            cyclic_reflection = false;
            break;
        }
    }
    std::cout << "VALID\n";
    std::cout << "order " << prototype.order << '\n';
    std::cout << "colors " << prototype.clique_sizes.size() << '\n';
    std::cout << "cyclic_reflection "
              << (cyclic_reflection ? "true" : "false") << '\n';
    return 0;
}

}  // namespace

int main(int argc, char** argv) {
    if (argc != 2) {
        std::cerr << "usage: verify_linear_prototype_cpp PROTOTYPE\n";
        return 2;
    }
    try {
        return verify(parse(argv[1]));
    } catch (const std::exception& error) {
        std::cout << "INVALID\nreason malformed_prototype\n";
        std::cout << "message " << error.what() << '\n';
        return 2;
    }
}
