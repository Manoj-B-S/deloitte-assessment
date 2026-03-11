/**
 * Deloitte Graduate Hiring – Java & API Development Assessment
 * =============================================================
 * Candidate  : Manoj B S
 * Email      : bsmanoj65@gmail.com
 * College    : Alliance University, Bangalore
 * Skill Track: Java & API Development
 *
 * Tasks Covered:
 *  1. OOP – Employee Management System
 *  2. Data Structures – Stack, Queue, LinkedList
 *  3. Algorithms – Sorting & Searching
 *  4. REST API Simulation (HTTP Server)
 *  5. Exception Handling & File I/O
 */

import com.sun.net.httpserver.HttpExchange;
import com.sun.net.httpserver.HttpHandler;
import com.sun.net.httpserver.HttpServer;

import java.io.*;
import java.net.InetSocketAddress;
import java.nio.charset.StandardCharsets;
import java.util.*;
import java.util.stream.Collectors;

public class Main {

    public static void main(String[] args) throws Exception {
        System.out.println("=".repeat(60));
        System.out.println("Deloitte Java & API Development Assessment");
        System.out.println("=".repeat(60));

        task1_OOP();
        task2_DataStructures();
        task3_Algorithms();
        task4_FileIO();
        task5_StartAPIServer();
    }

    // ─────────────────────────────────────────────────────────
    // TASK 1 – OOP: Employee Management
    // ─────────────────────────────────────────────────────────
    static void task1_OOP() {
        System.out.println("\n--- TASK 1: OOP – Employee Management System ---");

        List<Employee> employees = new ArrayList<>(Arrays.asList(
            new FullTimeEmployee("Rahul Sharma",   "Engineering", 75000),
            new FullTimeEmployee("Priya Patel",    "Design",      68000),
            new ContractEmployee("Amit Kumar",     "QA",          500, 160),
            new ContractEmployee("Sneha Reddy",    "Marketing",   450, 120),
            new FullTimeEmployee("Vikram Nair",    "Engineering", 82000),
            new FullTimeEmployee("Ananya Singh",   "HR",          60000)
        ));

        System.out.println("\nAll Employees:");
        employees.forEach(e -> System.out.printf("  %-20s | %-12s | Salary: ₹%,.0f%n",
                e.getName(), e.getDepartment(), e.calculateSalary()));

        double avg = employees.stream()
                              .mapToDouble(Employee::calculateSalary)
                              .average().orElse(0);
        System.out.printf("%nAverage Salary : ₹%,.2f%n", avg);

        Employee highest = employees.stream()
                                    .max(Comparator.comparingDouble(Employee::calculateSalary))
                                    .orElseThrow();
        System.out.printf("Highest Earner : %s (₹%,.0f)%n",
                highest.getName(), highest.calculateSalary());

        Map<String, Double> byDept = employees.stream()
            .collect(Collectors.groupingBy(Employee::getDepartment,
                     Collectors.averagingDouble(Employee::calculateSalary)));
        System.out.println("\nAverage salary by department:");
        byDept.forEach((dept, sal) ->
                System.out.printf("  %-14s : ₹%,.2f%n", dept, sal));
    }

    // ─────────────────────────────────────────────────────────
    // TASK 2 – Data Structures
    // ─────────────────────────────────────────────────────────
    static void task2_DataStructures() {
        System.out.println("\n--- TASK 2: Data Structures – Stack, Queue, LinkedList ---");

        // Stack
        System.out.println("\n[Stack – Balanced Parentheses Checker]");
        String[] exprs = {"({[]})", "({[}])", "((()))", "((()", "[]{}()"};
        for (String expr : exprs) {
            System.out.printf("  %10s -> %s%n", expr, isBalanced(expr) ? "VALID ✓" : "INVALID ✗");
        }

        // Queue – Task Scheduler
        System.out.println("\n[Queue – Task Scheduler Simulation]");
        Queue<String> taskQueue = new LinkedList<>(Arrays.asList(
                "Build Docker Image", "Run Unit Tests", "Deploy to Staging",
                "Smoke Test", "Deploy to Production"));
        System.out.println("  Processing tasks:");
        while (!taskQueue.isEmpty()) {
            System.out.println("  ✔ Completed: " + taskQueue.poll());
        }

        // Custom Linked List
        System.out.println("\n[Custom Singly Linked List]");
        CustomLinkedList<Integer> list = new CustomLinkedList<>();
        for (int v : new int[]{10, 20, 30, 40, 50}) list.add(v);
        System.out.println("  List     : " + list);
        list.remove(30);
        System.out.println("  After del: " + list);
        System.out.println("  Contains 40? " + list.contains(40));
        System.out.println("  Contains 30? " + list.contains(30));
        list.reverse();
        System.out.println("  Reversed : " + list);
    }

    static boolean isBalanced(String s) {
        Deque<Character> stack = new ArrayDeque<>();
        Map<Character, Character> pairs = Map.of(')', '(', '}', '{', ']', '[');
        for (char c : s.toCharArray()) {
            if ("({[".indexOf(c) >= 0) { stack.push(c); }
            else if (pairs.containsKey(c)) {
                if (stack.isEmpty() || stack.pop() != pairs.get(c)) return false;
            }
        }
        return stack.isEmpty();
    }

    // ─────────────────────────────────────────────────────────
    // TASK 3 – Algorithms
    // ─────────────────────────────────────────────────────────
    static void task3_Algorithms() {
        System.out.println("\n--- TASK 3: Algorithms – Sorting & Searching ---");

        int[] arr = {64, 25, 12, 22, 11, 90, 45, 33, 78, 55};
        System.out.println("Original : " + Arrays.toString(arr));

        // Bubble Sort
        int[] bubble = arr.clone();
        bubbleSort(bubble);
        System.out.println("Bubble   : " + Arrays.toString(bubble));

        // Merge Sort
        int[] merge = arr.clone();
        mergeSort(merge, 0, merge.length - 1);
        System.out.println("Merge    : " + Arrays.toString(merge));

        // Binary Search
        int target = 45;
        int idx = binarySearch(merge, target);
        System.out.printf("Binary Search for %d: found at index %d%n", target, idx);

        // Fibonacci (memoized)
        System.out.println("\n[Fibonacci – Memoized]");
        Map<Integer, Long> memo = new HashMap<>();
        for (int i : new int[]{5, 10, 20, 30, 40, 50}) {
            System.out.printf("  fib(%2d) = %d%n", i, fib(i, memo));
        }
    }

    static void bubbleSort(int[] a) {
        int n = a.length;
        for (int i = 0; i < n - 1; i++)
            for (int j = 0; j < n - i - 1; j++)
                if (a[j] > a[j + 1]) { int t = a[j]; a[j] = a[j+1]; a[j+1] = t; }
    }

    static void mergeSort(int[] a, int l, int r) {
        if (l >= r) return;
        int m = (l + r) / 2;
        mergeSort(a, l, m); mergeSort(a, m + 1, r);
        int[] tmp = new int[r - l + 1];
        int i = l, j = m + 1, k = 0;
        while (i <= m && j <= r) tmp[k++] = (a[i] <= a[j]) ? a[i++] : a[j++];
        while (i <= m) tmp[k++] = a[i++];
        while (j <= r) tmp[k++] = a[j++];
        System.arraycopy(tmp, 0, a, l, tmp.length);
    }

    static int binarySearch(int[] a, int target) {
        int lo = 0, hi = a.length - 1;
        while (lo <= hi) {
            int mid = (lo + hi) / 2;
            if (a[mid] == target) return mid;
            else if (a[mid] < target) lo = mid + 1;
            else hi = mid - 1;
        }
        return -1;
    }

    static long fib(int n, Map<Integer, Long> memo) {
        if (n <= 1) return n;
        return memo.computeIfAbsent(n, k -> fib(k - 1, memo) + fib(k - 2, memo));
    }

    // ─────────────────────────────────────────────────────────
    // TASK 4 – Exception Handling & File I/O
    // ─────────────────────────────────────────────────────────
    static void task4_FileIO() {
        System.out.println("\n--- TASK 4: Exception Handling & File I/O ---");
        String filePath = "candidate_info.txt";

        // Write
        try (PrintWriter pw = new PrintWriter(new FileWriter(filePath))) {
            pw.println("Full Name   : [Your Full Name]");
            pw.println("Email ID    : [Your Email]");
            pw.println("College     : [Your College Name]");
            pw.println("Skill Track : Java & API Development");
            pw.println("Assessment  : Completed");
            System.out.println("  File written: " + filePath);
        } catch (IOException e) {
            System.err.println("  Write error: " + e.getMessage());
        }

        // Read back
        try (BufferedReader br = new BufferedReader(new FileReader(filePath))) {
            System.out.println("  File contents:");
            br.lines().forEach(line -> System.out.println("    " + line));
        } catch (IOException e) {
            System.err.println("  Read error: " + e.getMessage());
        }

        // Custom exception demo
        System.out.println("\n  [Custom Exception Demo]");
        try {
            validateAge(-5);
        } catch (InvalidAgeException e) {
            System.out.println("  Caught: " + e.getMessage());
        }
        try {
            validateAge(25);
            System.out.println("  Age 25 is valid ✓");
        } catch (InvalidAgeException e) {
            System.out.println("  Caught: " + e.getMessage());
        }
    }

    static void validateAge(int age) throws InvalidAgeException {
        if (age < 0 || age > 120)
            throw new InvalidAgeException("Invalid age: " + age + ". Must be 0–120.");
    }

    // ─────────────────────────────────────────────────────────
    // TASK 5 – REST API Server (HTTP)
    // ─────────────────────────────────────────────────────────
    static final Map<Integer, String> employeeDB = new LinkedHashMap<>(Map.of(
        1, "{\"id\":1,\"name\":\"Rahul Sharma\",\"dept\":\"Engineering\",\"salary\":75000}",
        2, "{\"id\":2,\"name\":\"Priya Patel\",\"dept\":\"Design\",\"salary\":68000}",
        3, "{\"id\":3,\"name\":\"Amit Kumar\",\"dept\":\"QA\",\"salary\":60000}"
    ));

    static void task5_StartAPIServer() throws Exception {
        int port = 8080;
        HttpServer server = HttpServer.create(new InetSocketAddress(port), 0);

        server.createContext("/api/employees", new HttpHandler() {
            @Override
            public void handle(HttpExchange ex) throws IOException {
                String method = ex.getRequestMethod();
                String path   = ex.getRequestURI().getPath();
                String[] parts = path.split("/");
                String body; int status;

                if (method.equals("GET")) {
                    if (parts.length == 4) {
                        try {
                            int id = Integer.parseInt(parts[3]);
                            if (employeeDB.containsKey(id)) {
                                body = employeeDB.get(id); status = 200;
                            } else {
                                body = "{\"error\":\"Employee not found\"}"; status = 404;
                            }
                        } catch (NumberFormatException e) {
                            body = "{\"error\":\"Invalid ID\"}"; status = 400;
                        }
                    } else {
                        body = "[" + String.join(",", employeeDB.values()) + "]";
                        status = 200;
                    }
                } else {
                    body = "{\"error\":\"Method not allowed\"}"; status = 405;
                }

                byte[] bytes = body.getBytes(StandardCharsets.UTF_8);
                ex.getResponseHeaders().set("Content-Type", "application/json");
                ex.sendResponseHeaders(status, bytes.length);
                try (OutputStream os = ex.getResponseBody()) { os.write(bytes); }
            }
        });

        server.createContext("/api/health", ex -> {
            String resp = "{\"status\":\"UP\",\"service\":\"Deloitte Assessment API\"}";
            byte[] bytes = resp.getBytes(StandardCharsets.UTF_8);
            ex.getResponseHeaders().set("Content-Type", "application/json");
            ex.sendResponseHeaders(200, bytes.length);
            try (OutputStream os = ex.getResponseBody()) { os.write(bytes); }
        });

        server.setExecutor(null);
        server.start();

        System.out.println("\n--- TASK 5: REST API Server ---");
        System.out.println("  Server running on http://localhost:" + port);
        System.out.println("  Endpoints:");
        System.out.println("    GET /api/health            → Health check");
        System.out.println("    GET /api/employees         → All employees");
        System.out.println("    GET /api/employees/{id}    → Employee by ID");
        System.out.println("\n  Press ENTER to shut down server...");

        new BufferedReader(new InputStreamReader(System.in)).readLine();
        server.stop(0);
        System.out.println("  Server stopped.");
        System.out.println("\n" + "=".repeat(60));
        System.out.println("  ALL TASKS COMPLETED SUCCESSFULLY");
        System.out.println("  Candidate: [Your Full Name] | Track: Java & API Development");
        System.out.println("=".repeat(60));
    }
}

// ─── Supporting Classes ───────────────────────────────────────

abstract class Employee {
    private final String name;
    private final String department;

    Employee(String name, String department) {
        this.name = Objects.requireNonNull(name);
        this.department = Objects.requireNonNull(department);
    }

    public String getName()       { return name; }
    public String getDepartment() { return department; }
    public abstract double calculateSalary();

    @Override
    public String toString() {
        return String.format("Employee{name='%s', dept='%s', salary=%.0f}",
                name, department, calculateSalary());
    }
}

class FullTimeEmployee extends Employee {
    private final double monthlySalary;
    FullTimeEmployee(String name, String dept, double monthly) {
        super(name, dept); this.monthlySalary = monthly;
    }
    @Override public double calculateSalary() { return monthlySalary; }
}

class ContractEmployee extends Employee {
    private final double hourlyRate;
    private final int    hoursWorked;
    ContractEmployee(String name, String dept, double rate, int hours) {
        super(name, dept); this.hourlyRate = rate; this.hoursWorked = hours;
    }
    @Override public double calculateSalary() { return hourlyRate * hoursWorked; }
}

class CustomLinkedList<T> {
    private static class Node<T> { T data; Node<T> next; Node(T d) { data = d; } }
    private Node<T> head;

    public void add(T val) {
        if (head == null) { head = new Node<>(val); return; }
        Node<T> cur = head;
        while (cur.next != null) cur = cur.next;
        cur.next = new Node<>(val);
    }

    public boolean remove(T val) {
        if (head == null) return false;
        if (head.data.equals(val)) { head = head.next; return true; }
        Node<T> cur = head;
        while (cur.next != null) {
            if (cur.next.data.equals(val)) { cur.next = cur.next.next; return true; }
            cur = cur.next;
        }
        return false;
    }

    public boolean contains(T val) {
        Node<T> cur = head;
        while (cur != null) { if (cur.data.equals(val)) return true; cur = cur.next; }
        return false;
    }

    public void reverse() {
        Node<T> prev = null, cur = head;
        while (cur != null) { Node<T> nxt = cur.next; cur.next = prev; prev = cur; cur = nxt; }
        head = prev;
    }

    @Override
    public String toString() {
        StringBuilder sb = new StringBuilder("[");
        Node<T> cur = head;
        while (cur != null) { sb.append(cur.data); if (cur.next != null) sb.append(" -> "); cur = cur.next; }
        return sb.append("]").toString();
    }
}

class InvalidAgeException extends Exception {
    InvalidAgeException(String msg) { super(msg); }
}
