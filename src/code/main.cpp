#include <iostream>
#include <fstream>
#include <vector>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include <math.h>
#include <random>


// 反转
void reverseVector(std::vector<int32_t> &index,int i, int j) {
    while (i < j) {
        if (i < 0 || j < 0 || i >= index.size() || j >= index.size()) {
            break;
        }
        std::swap(index[i],index[j]);
        i++;
        j--;
    }
}

//把index[i]插入到index[j]后
void insertionVector(std::vector<int32_t> &index,int i, int j) {
    if (i < j) {
        index.insert(index.begin() + j, index[i]);
        index.erase(index.begin() + i);
    } else if (i > j) {
        int32_t temp = index[i];
        index.erase(index.begin() + i);
        index.insert(index.begin() + j, temp);
    }
}
std::vector<std::string> splitstr(std::string str, std::string deli = " ") {
    int32_t start = 0;
    int32_t end = str.find(deli);
    std::vector<std::string> vec;
    while (end != -1) {
        vec.push_back(str.substr(start, end - start));
        start = end + deli.size();
        end = str.find(deli, start);
    }
    vec.push_back(str.substr(start, end - start));
    return vec;
}

struct Point {
    Point(int32_t _id, std::string _name, double _x, double _y) {
        id = _id;
        name = _name;
        x = _x;
        y = _y;
    }
    Point(std::string  _id, std::string _name, std::string _x, std::string _y) {
        id = std::stoi(_id);
        name = _name;
        x = std::stod(_x);
        y = std::stod(_y);
    }

    int32_t id;
    std::string name;
    double x;
    double y;
};

//模拟退火算法(Simulated Annealing)
class SA{
public:
    SA(std::vector<Point> points) {
        points_ = points;
        T0_ = 50000.0 ; // 初始温度
        T_end_ = 1e-3; // 结束的温度
        q_ = 0.98;   // 退火系数
        L_ = 1000;  // 每个温度时的迭代次数，即链长
        N_ = points.size();  // 配送路径的总长度
        min_path_ = 1e9;
    }
    ReBuild() {
        work();
    }
    double path() {
        return min_path_;
    }
    void print_ans() {
        std::cout << "path_len:" << min_path_  << "km" << std::endl;
        std::fstream file_date;
        std::string file_name = "../小区配送路径.txt";
        file_date.open(file_name, std::ios::out);
        file_date << "path_len:" << get_path_len(min_index_)  << "km" << std::endl;
        int num = 0;
        for (auto index : min_index_) {
            std::cout << points_[index].id << " ";
            file_date << points_[index].name << " -> ";
            num++;
            if(num == 10) {
                file_date << "\n";
                num = 0;
            }
        }
        file_date << points_[0].name;
    }
private:
    double get_distance(Point p1, Point p2) {
        double dis_x = fabs(p1.x - p2.x);
        double dis_y = fabs(p1.y - p2.y);
        return sqrt(dis_x * dis_x + dis_y * dis_y);
    }
    //传入配送顺序
    double get_path_len(std::vector<int32_t> index) {
        if (index.size() != points_.size()) {
            std::cout << "get path len fail" << std::endl;
        }
        double path = 0.0;
        for (size_t i = 0; i < index.size() - 1; ++i) {
            Point point_now = points_[index[i]];
            Point point_next = points_[index[i+1]];
            path += get_distance(point_now, point_next);
        }
        //返回起点
        path += get_distance(points_[0], points_[index.size() - 1]);
        return path;
    }

    void creat_new_index(int case_) {
        int i = 1 + (rand() % (N_ - 1));
        int j = 1 + (rand() % (N_ - 1));
        if (case_ == 0) {
            std::swap(index_[i],index_[j]);
        } else if (case_ == 1) {
            if (i > j) {
                std::swap(i,j);
            }
            reverseVector(index_, i, j);
        } else if (case_ == 2) {
            insertionVector(index_, i, j);
        }
    }
    void init(int n) {
        if (min_index_.size() > 0) {
            index_ = min_index_;
            return;
        }
        index_.clear();
        for (int i = 0; i < n; ++i) {
            index_.push_back(i);
        }
//        return index_;
    }
    void work() {
        srand(time(0));
        std::cout << "begin solve sa" << std::endl;
        double start = clock(); // 程序运行开始计时
        double T;
        int count = 0; // 记录降温次数
        T = T0_; //初始温度
        init(N_); //初始化一个解
        auto copy_index = index_;
        double f1,f2,df; //f1为初始解目标函数值，
        //f2为新解目标函数值，df为二者差值
        double r; // 0-1之间的随机数，用来决定是否接受新解
        std::cout << "begin loop" << std::endl;
        while(T > T_end_) // 当温度低于结束温度时，退火结束
        {
            for(int i=0;i<L_;i++)
            {
//                print_ans();
                copy_index = index_;
                int case_ = rand() % 3;
                creat_new_index(case_); // 产生新解
                f1 = get_path_len(copy_index);
                f2 = get_path_len(index_);
                df = f2 - f1;
                // 以下是Metropolis准则
                if(df >= 0)
                {
                    r = 1.0 * rand() / RAND_MAX;
                    if(exp(-df/T) <= r) // 保留原来的解
                    {
                        index_ = copy_index;
                    }
                }
                if (min_path_ > f1) {
                    min_path_ = f1;
                    min_index_ = index_;
                }
            }
            T *= q_; // 降温
//            std::cout << "T:" << T << std::endl;
            count++;
        }
        std::cout << "end solve sa" << std::endl;

        double finish = clock(); // 退火过程结束
        duration_ = (finish-start) * 1.0 /CLOCKS_PER_SEC; // 计算时间
        std::cout << "duration:" << duration_ << "s" << std::endl;
        std::cout << "min_path:" << min_path_ << "km" << std::endl;
    }
    double T0_;
    double T_end_;
    double q_;
    int32_t L_;
    int32_t N_;
    std::vector<Point> points_;
    std::vector<int32_t> index_;
    double duration_;
    std::vector<int32_t> min_index_;
    double min_path_;
};

std::pair<double, double> get_center_point(std::vector<Point> points) {
    int32_t n = points.size();
    double center_x = 0.0;
    double center_y = 0.0;
    for (auto point : points) {
        center_x += point.x;
        center_y += point.y;
    }
    center_x /= n;
    center_y /= n;
    return std::make_pair(center_x, center_y);
}

void read_and_parse() {
    std::fstream file_date;
    std::string file_name = "../date_futian.txt";
    file_date.open(file_name, std::ios::in);
    std::vector<Point> points;
    if (!file_date.good()) {
        std::cout << "error" << std::endl;
    } else {
        std::cout << "read success" << std::endl;
        while(file_date) {
            std::string temp;
            file_date >> temp;
            auto vec = splitstr(temp, ",");
            if (vec.size() == 5) {
                Point point(vec[0],vec[2],vec[3],vec[4]);
                points.push_back(point);
            }
        }
        auto ans = get_center_point(points);
        std::cout << "center:" << ans.first << " " << ans.second << std::endl;
        Point begin_point(0 ,"配送站", ans.first, ans.second);
        points.insert(points.begin(), begin_point);

        std::cout << "point_size:" << points.size() << std::endl;
    }
    SA sa(points);
    int size_ = 0;
    while (sa.path() > 290) {
        sa.ReBuild();
        size_++;
        if (size_ > 20 || sa.path() < 290) {
            sa.print_ans();
            break;
        }
    }
}


int main() {
//    std::cout << rand(1,2);
    read_and_parse();
    return 0;
}
