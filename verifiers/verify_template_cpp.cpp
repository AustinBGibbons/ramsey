// Independent verifier for a Rowley-style effective (5,5,3) template.
//
// Candidate format (ASCII, keys may occur in any order):
//
//   order 94
//   phi_min 40
//   repeat_span 368
//   colors 112...3
//
// The colors value is one contiguous word of exactly order-1 symbols from
// {1,2,3}.  Symbols 1 and 2 are the two K_5-forbidden colors; symbol 3 is
// the triangle-forbidden template color.  Blank lines and text following
// '#' are ignored.  Duplicate keys, unknown keys, and extra tokens are
// rejected.
//
// This checker deliberately uses explicit candidate-list intersection for
// clique search.  It does not use a SAT solver, a bitset clique routine, or
// any project search code.

#include <algorithm>
#include <cctype>
#include <cstdint>
#include <fstream>
#include <iostream>
#include <limits>
#include <optional>
#include <sstream>
#include <stdexcept>
#include <string>
#include <vector>

namespace {

struct Candidate {
    int order = 0;
    int phi_min = 0;
    int repeat_span = 0;
    std::string colors;
};

struct ParseState {
    bool saw_order = false;
    bool saw_phi_min = false;
    bool saw_repeat_span = false;
    bool saw_colors = false;
};

class InputError : public std::runtime_error {
  public:
    using std::runtime_error::runtime_error;
};

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

int parse_int_strict(const std::string& token, const std::string& key,
                     int line_number) {
    std::size_t consumed = 0;
    long long value = 0;
    try {
        value = std::stoll(token, &consumed, 10);
    } catch (const std::exception&) {
        throw InputError("line " + std::to_string(line_number) +
                         ": value for " + key + " is not an integer");
    }
    if (consumed != token.size()) {
        throw InputError("line " + std::to_string(line_number) +
                         ": value for " + key + " is not an integer");
    }
    if (value < std::numeric_limits<int>::min() ||
        value > std::numeric_limits<int>::max()) {
        throw InputError("line " + std::to_string(line_number) +
                         ": value for " + key + " is outside int range");
    }
    return static_cast<int>(value);
}

Candidate parse_candidate(const std::string& path) {
    std::ifstream input(path);
    if (!input) {
        throw InputError("cannot open candidate file: " + path);
    }

    Candidate candidate;
    ParseState state;
    std::string raw_line;
    int line_number = 0;

    while (std::getline(input, raw_line)) {
        ++line_number;
        const std::size_t comment = raw_line.find('#');
        if (comment != std::string::npos) {
            raw_line.erase(comment);
        }
        const std::string line = trim(raw_line);
        if (line.empty()) {
            continue;
        }

        std::istringstream fields(line);
        std::string key;
        std::string value;
        std::string extra;
        if (!(fields >> key >> value) || (fields >> extra)) {
            throw InputError("line " + std::to_string(line_number) +
                             ": expected exactly '<key> <value>'");
        }

        if (key == "order") {
            if (state.saw_order) {
                throw InputError("line " + std::to_string(line_number) +
                                 ": duplicate key order");
            }
            state.saw_order = true;
            candidate.order = parse_int_strict(value, key, line_number);
        } else if (key == "phi_min") {
            if (state.saw_phi_min) {
                throw InputError("line " + std::to_string(line_number) +
                                 ": duplicate key phi_min");
            }
            state.saw_phi_min = true;
            candidate.phi_min = parse_int_strict(value, key, line_number);
        } else if (key == "repeat_span") {
            if (state.saw_repeat_span) {
                throw InputError("line " + std::to_string(line_number) +
                                 ": duplicate key repeat_span");
            }
            state.saw_repeat_span = true;
            candidate.repeat_span = parse_int_strict(value, key, line_number);
        } else if (key == "colors") {
            if (state.saw_colors) {
                throw InputError("line " + std::to_string(line_number) +
                                 ": duplicate key colors");
            }
            state.saw_colors = true;
            candidate.colors = value;
        } else {
            throw InputError("line " + std::to_string(line_number) +
                             ": unknown key " + key);
        }
    }

    if (!state.saw_order || !state.saw_phi_min ||
        !state.saw_repeat_span || !state.saw_colors) {
        std::string missing;
        if (!state.saw_order) {
            missing += " order";
        }
        if (!state.saw_phi_min) {
            missing += " phi_min";
        }
        if (!state.saw_repeat_span) {
            missing += " repeat_span";
        }
        if (!state.saw_colors) {
            missing += " colors";
        }
        throw InputError("missing required key(s):" + missing);
    }
    return candidate;
}

void emit_invalid(const std::string& reason) {
    std::cout << "INVALID\n";
    std::cout << "reason " << reason << '\n';
}

// For vertices u < v, return the periodically repeated base color of the
// positive distance v-u.  A distance divisible by p maps to base distance p.
int repeated_color(int u, int v, int p, const std::string& colors) {
    const int distance = v - u;
    const int residue = ((distance - 1) % p) + 1;
    return colors[static_cast<std::size_t>(residue - 1)] - '0';
}

// Search for a target-color clique using ordered candidate-list intersection.
// Every recursive candidate list is strictly increasing; hence each clique is
// visited at most once.  This is independent of bit-parallel clique routines.
bool find_clique_recursive(int target_color, int need,
                           const std::vector<int>& candidates,
                           std::vector<int>& chosen,
                           std::vector<int>& witness,
                           int p, const std::string& colors) {
    if (need == 0) {
        witness = chosen;
        return true;
    }
    if (static_cast<int>(candidates.size()) < need) {
        return false;
    }

    const int last_start =
        static_cast<int>(candidates.size()) - need;
    for (int index = 0; index <= last_start; ++index) {
        const int vertex = candidates[static_cast<std::size_t>(index)];
        std::vector<int> next;
        next.reserve(candidates.size() -
                     static_cast<std::size_t>(index + 1));
        for (std::size_t later = static_cast<std::size_t>(index + 1);
             later < candidates.size(); ++later) {
            const int other = candidates[later];
            if (repeated_color(vertex, other, p, colors) == target_color) {
                next.push_back(other);
            }
        }

        if (static_cast<int>(next.size()) < need - 1) {
            continue;
        }
        chosen.push_back(vertex);
        if (find_clique_recursive(target_color, need - 1, next,
                                  chosen, witness, p, colors)) {
            return true;
        }
        chosen.pop_back();
    }
    return false;
}

std::optional<std::vector<int>> find_repeated_k5(
    int target_color, int repeat_span, int p,
    const std::string& colors) {
    std::vector<int> candidates;
    candidates.reserve(static_cast<std::size_t>(repeat_span) + 1U);
    for (int vertex = 0; vertex <= repeat_span; ++vertex) {
        candidates.push_back(vertex);
    }
    std::vector<int> chosen;
    std::vector<int> witness;
    if (find_clique_recursive(target_color, 5, candidates, chosen,
                              witness, p, colors)) {
        return witness;
    }
    return std::nullopt;
}

void print_vertex_witness(int color, const std::vector<int>& vertices,
                          int p, const std::string& colors) {
    std::cout << "witness repeated_K5 color=" << color << " vertices=";
    for (std::size_t i = 0; i < vertices.size(); ++i) {
        if (i != 0U) {
            std::cout << ',';
        }
        std::cout << vertices[i];
    }
    std::cout << " edge_distances=";
    bool first = true;
    for (std::size_t i = 0; i < vertices.size(); ++i) {
        for (std::size_t j = i + 1; j < vertices.size(); ++j) {
            if (!first) {
                std::cout << ',';
            }
            first = false;
            const int distance = vertices[j] - vertices[i];
            const int residue = ((distance - 1) % p) + 1;
            std::cout << distance << "(r" << residue
                      << ":c" << colors[static_cast<std::size_t>(residue - 1)]
                      << ')';
        }
    }
    std::cout << '\n';
}

int verify(const Candidate& candidate) {
    if (candidate.order < 2) {
        emit_invalid("order_must_be_at_least_2");
        std::cout << "witness order=" << candidate.order << '\n';
        return 1;
    }
    if (candidate.phi_min < 0) {
        emit_invalid("phi_min_must_be_nonnegative");
        std::cout << "witness phi_min=" << candidate.phi_min << '\n';
        return 1;
    }
    if (candidate.repeat_span < 0) {
        emit_invalid("repeat_span_must_be_nonnegative");
        std::cout << "witness repeat_span=" << candidate.repeat_span << '\n';
        return 1;
    }
    // Avoid overflow in repeat_span+1 and pathological accidental inputs.
    if (candidate.repeat_span == std::numeric_limits<int>::max()) {
        emit_invalid("repeat_span_too_large");
        std::cout << "witness repeat_span=" << candidate.repeat_span << '\n';
        return 1;
    }

    const int p = candidate.order - 1;
    const std::int64_t required_repeat_span =
        4LL * static_cast<std::int64_t>(candidate.order - 2);
    if (static_cast<std::int64_t>(candidate.repeat_span) <
        required_repeat_span) {
        emit_invalid("repeat_span_below_required_4_times_order_minus_2");
        std::cout << "witness required=" << required_repeat_span
                  << " actual=" << candidate.repeat_span << '\n';
        return 1;
    }
    if (candidate.colors.size() != static_cast<std::size_t>(p)) {
        emit_invalid("wrong_color_word_length");
        std::cout << "witness expected=" << p
                  << " actual=" << candidate.colors.size() << '\n';
        return 1;
    }
    for (std::size_t index = 0; index < candidate.colors.size(); ++index) {
        const char symbol = candidate.colors[index];
        if (symbol != '1' && symbol != '2' && symbol != '3') {
            emit_invalid("color_outside_1_2_3");
            std::cout << "witness distance=" << (index + 1U)
                      << " symbol=" << symbol << '\n';
            return 1;
        }
    }

    if (candidate.colors[static_cast<std::size_t>(p - 1)] != '3') {
        emit_invalid("terminal_distance_not_in_T");
        std::cout << "witness distance=" << p
                  << " color="
                  << candidate.colors[static_cast<std::size_t>(p - 1)]
                  << '\n';
        return 1;
    }

    const int forbidden_prefix = std::min(candidate.phi_min, p);
    for (int distance = 1; distance <= forbidden_prefix; ++distance) {
        if (candidate.colors[static_cast<std::size_t>(distance - 1)] == '3') {
            emit_invalid("T_meets_forbidden_prefix");
            std::cout << "witness distance=" << distance
                      << " phi_min=" << candidate.phi_min << '\n';
            return 1;
        }
    }

    // Interval sum-freeness: a and b need not be distinct.
    for (int a = 1; a <= p; ++a) {
        if (candidate.colors[static_cast<std::size_t>(a - 1)] != '3') {
            continue;
        }
        for (int b = a; b <= p - a; ++b) {
            if (candidate.colors[static_cast<std::size_t>(b - 1)] == '3' &&
                candidate.colors[static_cast<std::size_t>(a + b - 1)] == '3') {
                emit_invalid("T_not_sum_free");
                std::cout << "witness a=" << a << " b=" << b
                          << " sum=" << (a + b) << '\n';
                return 1;
            }
        }
    }

    for (int color = 1; color <= 2; ++color) {
        const auto clique = find_repeated_k5(
            color, candidate.repeat_span, p, candidate.colors);
        if (clique.has_value()) {
            emit_invalid("repeated_color_contains_K5");
            print_vertex_witness(color, *clique, p, candidate.colors);
            return 1;
        }
    }

    int first_template_distance = p;
    int template_count = 0;
    for (int distance = 1; distance <= p; ++distance) {
        if (candidate.colors[static_cast<std::size_t>(distance - 1)] == '3') {
            first_template_distance =
                std::min(first_template_distance, distance);
            ++template_count;
        }
    }

    std::cout << "VALID\n";
    std::cout << "order " << candidate.order << '\n';
    std::cout << "period " << p << '\n';
    std::cout << "phi_min " << candidate.phi_min << '\n';
    std::cout << "actual_phi " << (first_template_distance - 1) << '\n';
    std::cout << "template_distance_count " << template_count << '\n';
    std::cout << "required_repeat_span " << required_repeat_span << '\n';
    std::cout << "repeat_span " << candidate.repeat_span << '\n';
    std::cout << "repeat_vertex_count " << (candidate.repeat_span + 1)
              << '\n';
    std::cout << "checked repeated_K5_colors=1,2 interval_sum_free_color=3\n";
    return 0;
}

}  // namespace

int main(int argc, char** argv) {
    if (argc != 2) {
        std::cerr << "usage: " << argv[0] << " CANDIDATE_FILE\n";
        return 2;
    }
    try {
        return verify(parse_candidate(argv[1]));
    } catch (const InputError& error) {
        std::cout << "INVALID\n";
        std::cout << "reason malformed_candidate\n";
        std::cout << "witness " << error.what() << '\n';
        return 2;
    } catch (const std::exception& error) {
        std::cerr << "verifier internal error: " << error.what() << '\n';
        return 3;
    }
}
