<?php

namespace App;

use PhpMcp\Server\Attributes\McpTool;
use PhpMcp\Server\Attributes\Schema;
use PhpMcp\Server\Attributes\McpPrompt;
use Psr\Log\LoggerInterface;

class CalculatorElements
{
    public function __construct(
        private readonly ?LoggerInterface $logger = null
    ) {
    }

    /**
     * WORLD 1 - AI ORCHESTRATES: Basic addition only.
     * This is called BY AI after reading the prompt instructions.
     * Returns raw number for AI to use in calculations.
     *
     * @param int $a The first number
     * @param int $b The second number
     * @return int The sum of a and b
     */
    #[McpTool(name: 'add_numbers', description: 'Add two numbers together (basic addition) - for AI orchestration')]
    public function addBasic(int $a, int $b): int
    {
        if ($this->logger) {
            $this->logger->info('Tool called: add_numbers (AI orchestration)', ['a' => $a, 'b' => $b]);
        }
        return $a + $b;
    }

    /**
     * WORLD 2 - TOOL ORCHESTRATES: Fast all-in-one calculation.
     * This tool does everything internally - no AI reasoning needed.
     * Use when you want guaranteed fast results.
     * 
     * Automatically executes:
     * 1. calculate_power to get a^b
     * 2. Addition to get a + b
     * 3. Combines both results
     * 4. Returns formatted answer
     *
     * @param int $a The first number (base for power, first addend)
     * @param int $b The second number (exponent for power, second addend)
     * @return string Combined result in words with emoji style
     */
    #[McpTool(name: 'hr_add_numbers_fast', description: 'Fast combined calculation (tool orchestrates everything)')]
    public function addFast(int $a, int $b): string
    {
        if ($this->logger) {
            $this->logger->info('Tool orchestrator: hr_add_numbers_fast', ['a' => $a, 'b' => $b]);
        }
        
        // Tool does all the work internally
        $powerResult = $this->power($a, $b);
        $additionResult = $a + $b;
        $combinedTotal = $powerResult + $additionResult;
        
        return "⚡ Fast Mode: The power result is $powerResult ($a^$b), the addition result is $additionResult ($a + $b), and the combined total is $combinedTotal. 😊";
    }

    /**
     * HYBRID: Smart calculation that supports both modes.
     * Default uses tool orchestration for speed.
     * Set $letAiOrchestrate=true to return instructions for AI.
     *
     * @param int $a The first number
     * @param int $b The second number  
     * @param bool $letAiOrchestrate If true, returns instructions for AI to follow
     * @return string|array Result or instructions
     */
    #[McpTool(name: 'hr_add_numbers', description: 'Smart calculation - supports both AI and tool orchestration')]
    public function add(int $a, int $b, bool $letAiOrchestrate = true): string|array
    {
        if ($letAiOrchestrate) {
            // WORLD 1: Let AI do the orchestration
            if ($this->logger) {
                $this->logger->info('AI orchestration mode activated', ['a' => $a, 'b' => $b]);
            }
            
            return [
                'mode' => 'ai_orchestration',
                'instructions' => "You are given two numbers: $a and $b.\n\nStep 1: Call 'calculate_power' with base=$a and exponent=$b.\nStep 2: Call 'add_numbers' with a=$a and b=$b.\nStep 3: Add both results together.\nStep 4: Present in words with emoji.",
                'hint' => 'AI should call calculate_power and add_numbers tools, then combine results'
            ];
        }
        
        // WORLD 2: Tool does everything (default, fast mode)
        if ($this->logger) {
            $this->logger->info('Tool orchestration mode (default)', ['a' => $a, 'b' => $b]);
        }
        
        $powerResult = $this->power($a, $b);
        $additionResult = $a + $b;
        $combinedTotal = $powerResult + $additionResult;
        
        return "🚀 Smart Mode: The power result is $powerResult ($a^$b), the addition result is $additionResult ($a + $b), and the combined total is $combinedTotal. 😊";
    }

    /**
     * Calculates power with validation.
     */
    #[McpTool(name: 'calculate_power')]
    public function power(
        #[Schema(type: 'number', minimum: 0, maximum: 1000)]
        float $base,
        
        #[Schema(type: 'integer', minimum: 0, maximum: 10)]
        int $exponent
    ): float {
        return pow($base, $exponent);
    }

    /**
     * Calculates 1 + 2.
     * 
     * @return int The result of 1 + 2
     */
    #[McpTool(name: 'calculate_one_plus_two')]
    public function calculateOnePlusTwo(): int
    {
        return 1 + 2;
    }

    #[McpTool(name: 'iics_get_employee_details',
    description:"Purpose: Retrieves comprehensive employee information from the HR system based on employee ID.
Functionality: This tool accepts an employee identifier and returns a structured dataset containing the employee's core information including their full name, assigned department, and current salary information.
Input Parameters:

employeeId (string, required): The unique identifier for the employee whose details are being requested

Output Schema:
The tool returns an associative array containing:

employeeId: The employee's unique identifier (string)
name: Employee's full name (string)
department: The department to which the employee is assigned (string)
salary: Current annual salary amount (numeric)

Use Cases:

HR information lookup and verification
Salary review and compensation analysis
Department staffing queries
Employee record validation
Integration with payroll and benefits systems

Security Considerations:

Requires appropriate access permissions to sensitive employee data
Should implement authentication and authorization checks
Salary information is confidential and subject to data privacy regulations")]
    public function getEmployeeDetails(string $employeeId): array
    {
        return [
            'employeeId' => $employeeId,
            'name' => 'John Doe',
            'department' => 'HR',
            'salary' => 100000,
        ];
    }



}