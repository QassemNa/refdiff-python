import java.io.File;
import java.util.ArrayList;

import refdiff.core.RefDiff;
import refdiff.core.cst.TokenPosition;
import refdiff.core.diff.CstDiff;
import refdiff.core.diff.Relationship;
import refdiff.parsers.python.PythonPlugin;

public class RefDiffExamplePythonlang {
    public static void main(String[] args) throws Exception {
        runExample();
    }

    private static void runExample() throws Exception {
        // This is a temp folder to clone or checkout git repositories.
        File tempFolder = new File("temp");

        // Creates a RefDiff instance configured with the Go plugin.
        try (PythonPlugin goPlugin = new PythonPlugin(tempFolder)) {
            RefDiff refDiffGo = new RefDiff(goPlugin);

            ArrayList<File> files= new ArrayList<>();
            files.add(refDiffGo.cloneGitRepository(
                    new File(tempFolder, "Mosallamy/python_refactoring_examples.git"),
                    "https://github.com/Mosallamy/python_refactoring_examples.git"));

            files.add(refDiffGo.cloneGitRepository(
                    new File(tempFolder, "QassemNa/python-refactoring-example.git"),
                    "https://github.com/QassemNa/python-refactoring-example.git"));

            for(File repo : files) {
                System.out.println("Starting a new Repo"+repo.getName());
                refDiffGo.computeDiffForCommitHistory(repo, 20, (commit, diff) -> {
                    printRefactorings("Refactorings found in Refactoring example " + commit.getId().name(), diff);
                });
            }
            
            //Delete the lines above from line 23 to line 37 and uncomment the lines below to run for a single commit
            
            //File repo = refDiffGo.cloneGitRepository(
            //        new File(tempFolder, "Mosallamy/python_refactoring_examples.git"),
            //        "https://github.com/Mosallamy/python_refactoring_examples.git");
            //CstDiff diffForCommit = refDiffGo.computeDiffForCommit(repo, "086c8ba803d7e398857000f6b000d075c7a2d910");
            //printRefactorings("Refactorings found in Python-refactoring-example 2f9137d5c06681ec885fb44a553e426c171bdd57", diffForCommit);
        }
    }

    private static void printRefactorings(String headLine, CstDiff diff) {
        System.out.println(headLine);
        for (Relationship rel : diff.getRefactoringRelationships()) {
            System.out.println(rel.getStandardDescription());
        }
    }
}
