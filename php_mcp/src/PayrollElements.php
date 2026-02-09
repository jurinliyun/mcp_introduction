<?php

namespace App;

use PhpMcp\Server\Attributes\McpTool;
use PhpMcp\Server\Attributes\Schema;

/**
 * Creates a connection to the local MySQL server.
 *
 * @return \mysqli|false Returns a mysqli object on success or false on failure.
 */
function getLocalMysqlConnection(): \mysqli|false
{
    $host = '127.0.0.1';
    $username = 'root';
    $password = 'root'; // Update this if your local MySQL has a password
    $database = 'iics_finance'; // Replace with your actual database name

    $mysqli = @new \mysqli($host, $username, $password, $database);

    if ($mysqli->connect_error) {
        // Handle connection error as you like (for now, return false)
        return false;
    }

    return $mysqli;
}


class PayrollElements
{
    /**
     * Calculates the payroll for a given employee.
     */
    #[McpTool(name: 'get_payslip', description: 'Get payslip for a given employee')]
    public function getPayslip(
        #[Schema(type: 'string')]
        string $employeeId,
        #[Schema(type: 'string')]
        string $month,
        #[Schema(type: 'string')]
        string $year,
    ): array
    {
        $mysqli = getLocalMysqlConnection();
        if ($mysqli === false) {
            return ['error' => 'Failed to connect to MySQL'];
        }

        // Use OR logic: search for payslip by either employee ID or employee name directly in salary slip join
        $query = "
            SELECT s.* 
            FROM `tabSalary Slip` s
            LEFT JOIN `tabEmployee` e ON s.employee = e.name
            WHERE 
                (
                    s.employee = ? OR 
                    e.employee_name = ?
                )
                AND s.`start_date` LIKE ?
                AND s.`end_date` LIKE ?
                AND s.docstatus = 1
            LIMIT 1
        ";
        $likePattern = "$year-$month-%";

        $stmt = $mysqli->prepare($query);
        if (!$stmt) {
            $mysqli->close();
            return ['error' => $mysqli->error];
        }
        // Bind both as same value (could be ID or name)
        $stmt->bind_param('ssss', $employeeId, $employeeId, $likePattern, $likePattern);
        $stmt->execute();
        $result = $stmt->get_result();
        $payslip = $result ? $result->fetch_assoc() : null;

        $mysqli->close();

        if (!$payslip) {
            return ['error' => 'No payslip found for this employee or employee name in given month/year'];
        }
        return $payslip;
    }


    #[McpTool(name: 'get_all_payslips', description: 'Get all payslips')]
    public function getAllPayslips(): array
    {
        $mysqli = getLocalMysqlConnection();
        if ($mysqli === false) {
            return ['error' => 'Failed to connect to MySQL'];
        }

        // Use OR logic: search for payslip by either employee ID or employee name directly in salary slip join
        $query = "
            SELECT s.* 
            FROM `tabSalary Slip` s
            LEFT JOIN `tabEmployee` e ON s.employee = e.name
            WHERE  s.docstatus = 1
            LIMIT 100
        ";
    

        $stmt = $mysqli->prepare($query);
        if (!$stmt) {
            $mysqli->close();
            return ['error' => $mysqli->error];
        }
        
        $stmt->execute();
        $result = $stmt->get_result();
        $payslip = $result ? $result->fetch_assoc() : null;

        $mysqli->close();

        if (!$payslip) {
            return ['error' => 'No payslips found'];
        }
        return $payslip;
    }
}