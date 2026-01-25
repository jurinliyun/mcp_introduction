<?php

namespace App;

use PhpMcp\Server\Attributes\McpTool;
use PhpMcp\Server\Attributes\Schema;

class CalculatorElements
{
    /**
     * Adds two numbers together.
     * 
     * @param int $a The first number
     * @param int $b The second number  
     * @return int The sum of the two numbers
     */
    #[McpTool(name: 'add_numbers')]
    public function add(int $a, int $b): int
    {
        return $a + $b;
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
}