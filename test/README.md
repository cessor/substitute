Setup, Exercise, Verify
=======================

The files in this folder describe the test for Substitute framework.
The features are split into the aforementioned phases, namely Setup, Exercise, Verify. 
 
 - ```Setup``` Is about configuring the Substitute for the following execution.
 - ```Exercise``` is all about providing data to the System under Test.
 - ```Verify``` is all about assertions. These functions help you to verify that calls have been made.

Background
----------
Any test can be described with four different phases: 

 - Setup
 - Exercise 
 - Verify
 - Teardown

First, you setup all the environmental conditions for your system under test to run.
Then, you exercise the System under Tast (a function or method, a class or many). Finally you verify, that the execution of the System under Test had the consequences that you expected (performed a calculation, changed some state, triggered another function). Eventually you should clean up after yourself, so that the next test to run is independent from previous results or state changes (this is done during the teardown phase). Have a look at Gerard Mezzaros excellent Book [xUnit Test Patterns - Refactoring Test Code](http://www.amazon.de/xUnit-Test-Patterns-Refactoring-Signature/dp/0131495054). There, you will find, that this Setup, Exercise, Verify split translates to other syntax you might know. 

<table class="table condensed">
	<thead>
		<tr>
			<th>xUTP</th>
			<th>AAA</th>
			<th>BDD</th>
		</tr>
	</thead>
	<tbody>
		<tr>
			<td>Setup</td>
			<td>Arrange</td>
			<td>Given</td>
		</tr>
		<tr>
			<td>Exercise</td>
			<td>Act</td>
			<td>When</td>
		</tr>
		<tr>
			<td>Verify</td>
			<td>Assert</td>
			<td>Then</td>
		</tr>
	</tbody>
</table>

Since Substitutes are dependent-on components they need to be set up, play a role during execution and help you verify interactions between components. Therefore the tests are also split after this scheme.