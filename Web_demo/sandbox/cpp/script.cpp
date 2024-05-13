#include <iostream>
#include <vector>
#include <cassert>

using namespace std;

vector<int> convolution(vector<int> a, vector<int> b) {
    int n = a.size();
    vector<int> c(2 * n - 1, 0);
    for(int i = 0; i < 2 * n - 1; ++i) {
        for(int j = max(0, i - n + 1); j <= min(i, n - 1); ++j) {
            c[i] += a[j] * b[i - j];
        }
    }
    return c;
}

void test_convolution() {
    // Test case 1
    {
        vector<int> a = {1, 2, 3};
        vector<int> b = {4, 5, 6};
        vector<int> expected = {4, 13, 28, 27, 18};
        assert(convolution(a, b) == expected);
    }

    // Test case 2: Negative values
    {
        vector<int> a = {-1, -2, -3};
        vector<int> b = {1, 2, 3};
        vector<int> expected = {-1, -4, -10, -8, -9};
        assert(convolution(a, b) == expected);
    }

    // Test case 3: Zeroes
    {
        vector<int> a = {0, 0, 0};
        vector<int> b = {1, 2, 3};
        vector<int> expected = {0, 0, 0, 0, 0};
        assert(convolution(a, b) == expected);
    }

    // Test case 4: Single element arrays
    {
        vector<int> a = {5};
        vector<int> b = {10};
        vector<int> expected = {50};
        assert(convolution(a, b) == expected);
    }

    // Test case 5: Different positive values
    {
        vector<int> a = {2, 4, 6};
        vector<int> b = {1, 3, 5};
        vector<int> expected = {2, 10, 28, 32, 30};
        assert(convolution(a, b) == expected);
    }

    // Test case 6: Larger arrays
    {
        vector<int> a = {1, 3, 5, 7};
        vector<int> b = {2, 4, 6, 8};
        vector<int> expected = {2, 10, 28, 52, 60, 58, 56};
        assert(convolution(a, b) == expected);
    }

    // Test case 7: Arrays with a negative and positive mix
    {
        vector<int> a = {-1, 2, -3, 4};
        vector<int> b = {5, -6, 7, -8};
        vector<int> expected = {-5, 16, -31, 58, -67, 52, -32};
        assert(convolution(a, b) == expected);
    }

    cout << "All test cases passed!" << endl;
}

int main() {
    test_convolution();
    return 0;
}